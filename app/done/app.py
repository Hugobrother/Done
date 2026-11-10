"""Process principal : icône dans la barre de menus / zone de notification + boucle de détection."""
import socket, sys, threading, time

import pystray
from PIL import Image, ImageDraw

from . import core, detectors

CONFIRM = 3      # vérifs sans bouton Stop avant de conclure
INTERVAL = 0.7   # secondes entre deux vérifs


def make_icon(size=64):
    """Bulle + point : version monochrome pour la barre de menus."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 64
    d.rounded_rectangle((4 * s, 14 * s, 60 * s, 46 * s), radius=16 * s, outline=(0, 0, 0, 255), width=int(5 * s))
    d.polygon([(10 * s, 40 * s), (6 * s, 56 * s), (22 * s, 44 * s)], fill=(0, 0, 0, 255))
    for x, a in ((18, 110), (30, 190)):
        d.ellipse(((x - 4) * s, 26 * s, (x + 4) * s, 34 * s), fill=(0, 0, 0, a))
    d.ellipse((38 * s, 21 * s, 52 * s, 39 * s), fill=(0, 0, 0, 255))
    return img


class Engine(threading.Thread):
    def __init__(self, state):
        super().__init__(daemon=True)
        self.state = state
        self.tracks = {}

    def run(self):
        if sys.platform == "win32":
            import uiautomation as auto
            with auto.UIAutomationInitializerInThread():
                self.loop()
        else:
            self.loop()

    def loop(self):
        while True:
            cfg = self.state["cfg"]
            try:
                seen = detectors.scan(cfg)
            except Exception as e:
                print("scan error:", e, file=sys.stderr)
                seen = {}
            now = time.time()
            for key, (stop, perm) in seen.items():
                t = self.tracks.setdefault(key, {"gen": False, "miss": 0, "start": 0, "ask": False})
                if perm and not t["ask"] and cfg["notify_approval"]:
                    core.send(cfg, cfg["text_approval"], cfg["loud_approval"], "warning")
                t["ask"] = perm
                if stop:
                    if not t["gen"]:
                        t["start"] = now
                    t["gen"], t["miss"] = True, 0
                elif t["gen"] and not perm:
                    t["miss"] += 1
                    if t["miss"] >= CONFIRM:
                        if cfg["notify_answered"] and now - t["start"] >= cfg["min_seconds"]:
                            core.send(cfg, cfg["text_answered"], cfg["loud_answered"], "white_check_mark")
                        t["gen"], t["miss"] = False, 0
            # fenêtres non vues (onglet changé, fenêtre fermée) : on garde l'état, on ne conclut rien
            time.sleep(INTERVAL)


PORT = 47812  # port local : une seule copie de done. à la fois
_hooks = {}   # "quit" -> fonction qui arrête l'icône


def _already_running():
    """Si done. tourne déjà, lui demande d'afficher sa fenêtre et renvoie True."""
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=0.5) as s:
            s.sendall(b"show")
        return True
    except OSError:
        return False


def _listen_for_show():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind(("127.0.0.1", PORT))
    except OSError:
        return
    srv.listen(4)

    def loop():
        while True:
            conn, _ = srv.accept()
            with conn:
                msg = conn.recv(16)
                if msg.startswith(b"show"):
                    core.open_window("settings")
                elif msg.startswith(b"quit") and "quit" in _hooks:
                    _hooks["quit"]()

    threading.Thread(target=loop, daemon=True).start()


def main():
    if _already_running():
        return  # l'instance existante ouvre sa fenêtre
    _listen_for_show()
    background = "--background" in sys.argv  # lancé au démarrage de l'ordi : silencieux
    state = {"cfg": core.load(), "mtime": core.mtime()}

    def reload_loop():
        while True:
            m = core.mtime()
            if m != state["mtime"]:
                state["cfg"], state["mtime"] = core.load(), m
                icon.update_menu()
            time.sleep(1)

    def toggle(key):
        def f(_icon, _item):
            c = core.load()
            c[key] = not c[key]
            core.save(c)
            if key == "autostart":
                core.set_autostart(c[key])
            state["cfg"], state["mtime"] = c, core.mtime()
        return f

    checked = lambda key: (lambda item: state["cfg"][key])

    def status_text(_):
        ok, msg = detectors.status()
        return ("● " if ok else "⚠ ") + msg

    def test(_icon, _item):
        core.send(state["cfg"], "Test ping from done. ✅", True, "tada")

    def quit_(icon_, _item):
        icon_.stop()

    menu = pystray.Menu(
        pystray.MenuItem(status_text, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Notify when Claude finishes", toggle("notify_answered"), checked=checked("notify_answered")),
        pystray.MenuItem("Notify on approval requests", toggle("notify_approval"), checked=checked("notify_approval")),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Watch Claude app", toggle("watch_app"), checked=checked("watch_app")),
        pystray.MenuItem("Watch claude.ai (browser)", toggle("watch_web"), checked=checked("watch_web")),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Pair phone…", lambda *_: core.open_window("pair")),
        pystray.MenuItem("Settings…", lambda *_: core.open_window("settings")),
        pystray.MenuItem("Send test notification", test),
        pystray.MenuItem("Start at login", toggle("autostart"), checked=checked("autostart")),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit done.", quit_),
    )

    icon = pystray.Icon("done", make_icon(), "done.", menu)
    _hooks["quit"] = icon.stop
    if sys.platform == "darwin":
        icon.icon = make_icon(44)

    # Premier lancement : permission + appairage
    if not state["cfg"]["onboarded"]:
        detectors.request_permission()
        core.set_autostart(state["cfg"]["autostart"])
        core.open_window("pair")
    elif not background:
        # ouvert à la main : on montre toujours une fenêtre (l'icône peut être cachée par l'encoche)
        core.open_window("settings")

    # Mac : la permission n'est prise en compte qu'au redémarrage -> on se relance tout seul
    if sys.platform == "darwin" and not detectors.status()[0]:
        def wait_permission():
            while not core.ax_trusted_fresh():
                time.sleep(2)
            core.relaunch_later()
            icon.stop()
        threading.Thread(target=wait_permission, daemon=True).start()

    Engine(state).start()
    threading.Thread(target=reload_loop, daemon=True).start()

    def setup(ic):
        ic.visible = True
        if sys.platform == "darwin":
            try:  # icône « template » : s'adapte au mode clair/sombre de la barre de menus
                ic._status_item.button().image().setTemplate_(True)
            except Exception:
                pass

    icon.run(setup=setup)
