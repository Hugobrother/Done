"""Détection « Claude écrit » / « Claude demande une autorisation »
dans l'app Claude desktop (Mac, Windows) et dans claude.ai sur le web (Mac, Windows, Linux).

scan(cfg) -> {source_id: (stop_visible, approval_visible)}
"""
import sys

STOP_WORDS = ("stop", "arrêter", "arreter", "detener", "stoppen")
ALLOW_WORDS = ("allow", "autoriser", "approve", "approuver", "permitir", "erlauben")
DENY_WORDS = ("deny", "refuser", "reject", "rejeter", "denegar", "ablehnen", "don't allow", "ne pas autoriser")
MAX_NODES = 8000


def classify(labels):
    short = [l for l in labels if l and len(l) < 40]
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
    import psutil
    import uiautomation as auto

    APP_EXES = {"claude.exe"}
    BROWSER_EXES = {"chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe", "vivaldi.exe", "arc.exe"}

    def request_permission():
        return True

    def status():
        return True, "Watching Claude"

    def scan(cfg):
        out = {}
        for w in auto.GetRootControl().GetChildren():
            try:
                exe = psutil.Process(w.ProcessId).name().lower()
            except Exception:
                continue
            is_app = exe in APP_EXES and cfg["watch_app"]
            is_web = exe in BROWSER_EXES and cfg["watch_web"]
            if not (is_app or is_web):
                continue
            if is_web and "claude" not in (w.Name or "").lower():
                continue
            labels, n = [], 0
            for c, _ in auto.WalkControl(w, maxDepth=80):
                n += 1
                if n > MAX_NODES:
                    break
                if c.ControlType == auto.ControlType.ButtonControl:
                    labels.append((c.Name or "").strip().lower())
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
