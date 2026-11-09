"""Détection « Claude écrit » / « Claude demande une autorisation »
dans l'app Claude desktop (Mac, Windows) et dans claude.ai sur le web (Mac, Windows, Linux).

scan(cfg) -> {source_id: (stop_visible, approval_visible)}
"""
import sys
import unicodedata

# Mots-clés SANS accents : les libellés sont normalisés avant comparaison
STOP_WORDS = ("stop", "arreter", "detener", "stoppen")
ALLOW_WORDS = ("allow", "autoriser", "approve", "approuver", "permitir", "erlauben")
DENY_WORDS = ("deny", "refuser", "reject", "rejeter", "denegar", "ablehnen", "don't allow", "ne pas autoriser")
MAX_NODES = 8000


def norm(s):
    """minuscules + sans accents ('Arrêter' -> 'arreter'), quel que soit l'encodage du ê"""
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).strip().lower()


def classify(labels):
    # libellés courts seulement : les boutons « actions du message » contiennent tout le texte
    short = [n for n in (norm(l) for l in labels) if n and len(n) < 40]
    has = lambda words: any(w in l for l in short for w in words)
    return has(STOP_WORDS), has(ALLOW_WORDS) and has(DENY_WORDS)


def _merge(out, key, stop, perm):
    s, p = out.get(key, (False, False))
    out[key] = (s or stop, p or perm)


# ======================================================================
if sys.platform == "darwin":
    from AppKit import NSWorkspace
    from ApplicationServices import (
        AXUIElementCreateApplication, AXUIElementCopyAttributeValue,
        AXUIElementSetAttributeValue, AXIsProcessTrusted, AXIsProcessTrustedWithOptions,
        kAXTrustedCheckOptionPrompt)

    APP_IDS = {"com.anthropic.claudefordesktop"}
    BROWSER_IDS = {
        "com.google.Chrome", "com.apple.Safari", "company.thebrowser.Browser", "com.microsoft.edgemac",
        "com.brave.Browser", "org.mozilla.firefox", "com.operasoftware.Opera", "com.vivaldi.Vivaldi",
        "org.chromium.Chromium",
    }

    def _attr(el, name):
        err, val = AXUIElementCopyAttributeValue(el, name, None)
        return val if err == 0 else None

    def _labels(root):
        out, stack, n = [], [(root, 0)], 0
        while stack and n < MAX_NODES:
            el, d = stack.pop()
            n += 1
            if _attr(el, "AXRole") == "AXButton":
                out.append(" ".join(str(_attr(el, a) or "") for a in ("AXTitle", "AXDescription", "AXHelp")).strip().lower())
            if d < 80:
                stack.extend((c, d + 1) for c in (_attr(el, "AXChildren") or []))
        return out

    def request_permission():
        return AXIsProcessTrustedWithOptions({kAXTrustedCheckOptionPrompt: True})

    def status():
        if AXIsProcessTrusted():
            return True, "Watching Claude"
        return False, "Accessibility permission needed"

    def scan(cfg):
        out = {}
        for app in NSWorkspace.sharedWorkspace().runningApplications():
            bid = app.bundleIdentifier()
            is_app = bid in APP_IDS and cfg["watch_app"]
            is_web = bid in BROWSER_IDS and cfg["watch_web"]
            if not (is_app or is_web):
                continue
            el = AXUIElementCreateApplication(app.processIdentifier())
            AXUIElementSetAttributeValue(el, "AXManualAccessibility", True)
            # AXWindows ne voit pas les fenêtres plein écran d'un autre bureau -> fenêtre principale
            wins = _attr(el, "AXWindows") or [w for w in (_attr(el, "AXMainWindow"), _attr(el, "AXFocusedWindow")) if w is not None][:1]
            for w in wins:
                if is_web and "claude" not in str(_attr(w, "AXTitle") or "").lower():
                    continue
                labels = _labels(w)
                if labels:
                    _merge(out, "app" if is_app else f"web:{bid}", *classify(labels))
        return out

# ======================================================================
elif sys.platform == "win32":
    # Méthode validée sur un vrai PC Windows :
    # - EnumWindows + PID : on n'interroge que les fenêtres Claude / navigateurs
    # - une seule requête UIA FindAll(Descendants, Bouton) par fenêtre
    # - try par bouton : ils disparaissent souvent pendant la génération
    import ctypes
    from ctypes import wintypes

    import psutil
    import uiautomation as auto  # noqa: F401  (initialise COM / UIA)

    try:
        from uiautomation.uiautomation import _AutomationClient
    except ImportError:
        _AutomationClient = auto._AutomationClient

    APP_EXES = {"claude.exe"}
    BROWSER_EXES = {"chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe", "vivaldi.exe", "arc.exe"}
    TREE_DESCENDANTS = 4          # TreeScope_Descendants
    PROP_CONTROL_TYPE = 30003     # UIA_ControlTypePropertyId
    TYPE_BUTTON = 50000           # UIA_ButtonControlTypeId

    user32 = ctypes.windll.user32
    ENUM_PROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    _uia = {}

    def _client():
        # créé dans le thread de détection (après l'init COM de ce thread)
        if "uia" not in _uia:
            uia = _AutomationClient.instance().IUIAutomation
            _uia["uia"] = uia
            _uia["cond"] = uia.CreatePropertyCondition(PROP_CONTROL_TYPE, TYPE_BUTTON)
        return _uia["uia"], _uia["cond"]

    def request_permission():
        return True

    def status():
        return True, "Watching Claude"

    def _windows(pids):
        """[(hwnd, pid, titre)] des fenêtres visibles appartenant à ces process."""
        found = []

        def cb(hwnd, _):
            n = user32.GetWindowTextLengthW(hwnd)
            if user32.IsWindowVisible(hwnd) and n > 0:
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if pid.value in pids:
                    buf = ctypes.create_unicode_buffer(n + 1)
                    user32.GetWindowTextW(hwnd, buf, n + 1)
                    found.append((hwnd, pid.value, buf.value))
            return True

        user32.EnumWindows(ENUM_PROC(cb), 0)
        return found

    def _labels(hwnd):
        uia, cond = _client()
        out = []
        try:
            arr = uia.ElementFromHandle(hwnd).FindAll(TREE_DESCENDANTS, cond)
            for i in range(min(arr.Length, MAX_NODES)):
                try:
                    name = arr.GetElement(i).CurrentName
                    if name:
                        out.append(name)
                except Exception:
                    pass  # bouton disparu pendant la lecture
        except Exception as e:
            print("uia error:", e, file=sys.stderr)
        return out

    def scan(cfg):
        wanted = {}
        for p in psutil.process_iter(["name"]):
            exe = (p.info["name"] or "").lower()
            if (exe in APP_EXES and cfg["watch_app"]) or (exe in BROWSER_EXES and cfg["watch_web"]):
                wanted[p.pid] = exe
        out = {}
        if not wanted:
            return out
        for hwnd, pid, title in _windows(set(wanted)):
            exe = wanted[pid]
            is_app = exe in APP_EXES
            if not is_app and "claude" not in title.lower():
                continue
            labels = _labels(hwnd)
            if labels:
                _merge(out, "app" if is_app else f"web:{exe}", *classify(labels))
        return out

# ======================================================================
else:  # Linux : AT-SPI (navigateurs ; pas d'app Claude officielle)
    import subprocess
    try:
        import gi
        gi.require_version("Atspi", "2.0")
        from gi.repository import Atspi
        _OK = True
    except Exception:
        _OK = False

    BROWSERS = ("chrome", "chromium", "firefox", "brave", "edge", "opera", "vivaldi")

    def request_permission():
        # Active l'accessibilité GNOME pour que les navigateurs exposent leurs boutons
        try:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "toolkit-accessibility", "true"], timeout=5)
        except Exception:
            pass
        return _OK

    def status():
        if not _OK:
            return False, "Install AT-SPI: sudo apt install gir1.2-atspi-2.0"
        return True, "Watching Claude (restart your browser once)"

    def _labels(root):
        out, stack, n = [], [(root, 0)], 0
        btn = {Atspi.Role.PUSH_BUTTON, Atspi.Role.TOGGLE_BUTTON}
        while stack and n < MAX_NODES:
            el, d = stack.pop()
            n += 1
            try:
                if el.get_role() in btn:
                    out.append((el.get_name() or "").strip().lower())
                if d < 80:
                    stack.extend((el.get_child_at_index(i), d + 1) for i in range(el.get_child_count()))
            except Exception:
                continue
        return out

    def scan(cfg):
        out = {}
        if not _OK:
            return out
        desk = Atspi.get_desktop(0)
        for i in range(desk.get_child_count()):
            app = desk.get_child_at_index(i)
            if app is None:
                continue
            name = (app.get_name() or "").lower()
            is_app = "claude" in name and cfg["watch_app"]
            is_web = any(b in name for b in BROWSERS) and cfg["watch_web"]
            if not (is_app or is_web):
                continue
            for j in range(app.get_child_count()):
                w = app.get_child_at_index(j)
                if w is None or (is_web and "claude" not in (w.get_name() or "").lower()):
                    continue
                labels = _labels(w)
                if labels:
                    _merge(out, "app" if is_app else f"web:{name}", *classify(labels))
        return out
