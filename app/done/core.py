"""Config, envoi ntfy, démarrage auto. Commun aux 3 OS."""
import json, os, sys, secrets, ssl, subprocess, urllib.request
from pathlib import Path

APP_NAME = "done."
PAIR_PAGE = "https://done-ad335.web.app/pair.html"

if sys.platform == "darwin":
    CONFIG_DIR = Path.home() / "Library" / "Application Support" / "done"
elif sys.platform == "win32":
    CONFIG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "done"
else:
    CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "done"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "server": "https://ntfy.sh",
    "topic": "",
    "notify_answered": True,
    "notify_approval": True,
    "text_answered": "[Claude] has answered",
    "text_approval": "[Claude] needs your approval",
    "loud_answered": True,
    "loud_approval": True,
    "min_seconds": 0,
    "watch_app": True,
    "watch_web": True,
    "autostart": True,
    "onboarded": False,
}


def load():
    cfg = dict(DEFAULTS)
    try:
        cfg.update(json.loads(CONFIG_FILE.read_text("utf-8")))
    except Exception:
        pass
    if not cfg["topic"]:
        cfg["topic"] = "done-" + secrets.token_urlsafe(12).replace("_", "x").lower()
        save(cfg)
    return cfg


def save(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CONFIG_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), "utf-8")
    os.replace(tmp, CONFIG_FILE)


def mtime():
    try:
        return CONFIG_FILE.stat().st_mtime
    except OSError:
        return 0


def pair_url(cfg):
    return f"{PAIR_PAGE}?t={cfg['topic']}"


def _ssl_context():
    # Les apps packagées n'ont pas accès aux certificats système : on embarque ceux de certifi
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


SSL_CTX = _ssl_context()


def send(cfg, text, loud=True, tag="white_check_mark"):
    """Envoie une notif ntfy. loud=True -> prio max (son + vibration), False -> prio min (silencieux)."""
    req = urllib.request.Request(
        f"{cfg['server'].rstrip('/')}/{cfg['topic']}",
        data=text.encode("utf-8"),
        headers={"Title": "done.", "Priority": "5" if loud else "1", "Tags": tag},
    )
    try:
        urllib.request.urlopen(req, timeout=10, context=SSL_CTX)
        return True
    except Exception as e:
        print("ntfy error:", e, file=sys.stderr)
        return False


# ---------- relancer le même exécutable pour ouvrir une fenêtre ----------
def self_cmd(*args):
    if getattr(sys, "frozen", False):
        return [sys.executable, *args]
    return [sys.executable, "-m", "done", *args]


def quit_running():
    """Demande à la copie de done. qui tourne de s'arrêter."""
    import socket
    try:
        with socket.create_connection(("127.0.0.1", 47812), timeout=0.5) as s:
            s.sendall(b"quit")
    except OSError:
        pass


def open_window(kind):
    subprocess.Popen(self_cmd("--ui", kind), cwd=str(Path(__file__).resolve().parent.parent))


# ---------- démarrage automatique ----------
def _exe_path():
    return sys.executable if getattr(sys, "frozen", False) else None


def set_autostart(enabled):
    exe = _exe_path()
    if not exe:
        return  # mode dev : on ne touche à rien
    try:
        if sys.platform == "darwin":
            app = Path(exe).resolve().parents[2]  # .../done.app
            plist = Path.home() / "Library/LaunchAgents/app.done.plist"
            if enabled:
                plist.parent.mkdir(parents=True, exist_ok=True)
                plist.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>app.done</string>
<key>ProgramArguments</key><array><string>/usr/bin/open</string><string>-g</string><string>{app}</string><string>--args</string><string>--background</string></array>
<key>RunAtLoad</key><true/>
</dict></plist>
""")
            elif plist.exists():
                plist.unlink()
        elif sys.platform == "win32":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            if enabled:
                winreg.SetValueEx(key, "done", 0, winreg.REG_SZ, f'"{exe}" --background')
            else:
                try:
                    winreg.DeleteValue(key, "done")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        else:
            f = Path.home() / ".config/autostart/done.desktop"
            if enabled:
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text(f"[Desktop Entry]\nType=Application\nName=done.\nExec=\"{exe}\" --background\nX-GNOME-Autostart-enabled=true\n")
            elif f.exists():
                f.unlink()
    except Exception as e:
        print("autostart error:", e, file=sys.stderr)
