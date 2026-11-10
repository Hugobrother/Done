"""Fenêtres (tkinter), lancées dans un process séparé : appairage et réglages."""
import sys
import tkinter as tk
from tkinter import ttk

import qrcode
from PIL import ImageTk

from . import core, detectors

BG, FG, MUTED, ACCENT = "#262624", "#FAF9F5", "#B8B5AD", "#D97757"


def _root(title):
    root = tk.Tk()
    root.title(title)
    root.configure(bg=BG, padx=28, pady=24)
    root.resizable(False, False)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    for w in ("TFrame", "TLabelframe"):
        style.configure(w, background=BG)
    style.configure("TLabelframe.Label", background=BG, foreground=FG, font=("Helvetica", 13, "bold"))
    style.configure("TLabel", background=BG, foreground=FG, font=("Helvetica", 13))
    style.configure("Muted.TLabel", foreground=MUTED, font=("Helvetica", 12))
    style.configure("H.TLabel", font=("Helvetica", 20, "bold"))
    style.configure("TCheckbutton", background=BG, foreground=FG, font=("Helvetica", 13))
    style.configure("TRadiobutton", background=BG, foreground=FG, font=("Helvetica", 13))
    style.map("TCheckbutton", background=[("active", BG)])
    style.map("TRadiobutton", background=[("active", BG)])
    style.configure("Accent.TButton", background=ACCENT, foreground="#1A1A19", font=("Helvetica", 13, "bold"), padding=(14, 8))
    style.map("Accent.TButton", background=[("active", "#E8A17F")])
    style.configure("TButton", font=("Helvetica", 13), padding=(12, 8))
    root.lift()
    root.attributes("-topmost", True)
    root.after(800, lambda: root.attributes("-topmost", False))
    root.focus_force()
    return root


# ----------------------------------------------------------------------
def pair_window():
    cfg = core.load()
    root = _root("done. — Pair your phone")

    ttk.Label(root, text="Pair your phone", style="H.TLabel").pack(anchor="w")
    ttk.Label(root, text="Takes about a minute. You only do this once.", style="Muted.TLabel").pack(anchor="w", pady=(2, 14))

    # Étape permission (Mac)
    perm = ttk.Label(root, text="", foreground=ACCENT)
    perm_btn = ttk.Button(root, text="Allow Accessibility", command=detectors.request_permission)

    def refresh_perm():
        ok, _ = detectors.status()
        if sys.platform == "darwin" and not ok:
            perm.config(text="⚠  Step 0: allow done. in Accessibility so it can see Claude.")
            perm.pack(anchor="w")
            perm_btn.pack(anchor="w", pady=(4, 12))
        else:
            perm.pack_forget()
            perm_btn.pack_forget()
        root.after(1500, refresh_perm)

    url = core.pair_url(cfg)
    img = qrcode.make(url, border=2, box_size=6).convert("RGB")
    photo = ImageTk.PhotoImage(img)

    row = ttk.Frame(root)
    row.pack(fill="x")
    tk.Label(row, image=photo, bg=BG).pack(side="left", padx=(0, 22))
    steps = ttk.Frame(row)
    steps.pack(side="left", fill="y")
    for i, t in enumerate([
        "Install the free ntfy app\n(App Store / Google Play).",
        "Scan this QR code with your\nphone camera.",
        "Follow the page: it subscribes\nntfy to your private channel.",
        "Tap “Send test” below.",
    ], 1):
        ttk.Label(steps, text=f"{i}.  {t}").pack(anchor="w", pady=4)

    ttk.Label(root, text=f"Channel: {cfg['topic']}", style="Muted.TLabel").pack(anchor="w", pady=(14, 0))

    status = ttk.Label(root, text="", style="Muted.TLabel")
    btns = ttk.Frame(root)
    btns.pack(fill="x", pady=(16, 0))

    def test():
        ok = core.send(cfg, "Test: your phone is paired ✅", loud=True, tag="tada")
        status.config(text="Sent! Check your phone." if ok else "Could not reach ntfy. Check your internet.")

    def done():
        c = core.load()
        c["onboarded"] = True
        core.save(c)
        root.destroy()

    ttk.Button(btns, text="Send test", style="Accent.TButton", command=test).pack(side="left")
    ttk.Button(btns, text="Done", command=done).pack(side="right")
    status.pack(anchor="w", pady=(8, 0))

    refresh_perm()
    root.protocol("WM_DELETE_WINDOW", done)
    root.mainloop()


# ----------------------------------------------------------------------
def settings_window():
    cfg = core.load()
    root = _root("done. — Settings")
    v = {k: (tk.BooleanVar(value=cfg[k]) if isinstance(cfg[k], bool) else tk.StringVar(value=str(cfg[k]))) for k in core.DEFAULTS if k not in ("server", "topic", "onboarded")}

    ttk.Label(root, text="Settings", style="H.TLabel").pack(anchor="w")
    where = {"darwin": "the bubble icon in your menu bar (top right; it can hide behind the notch)",
             "win32": "the bubble icon in your system tray (bottom right, maybe behind the ^ arrow)"}.get(
        sys.platform, "the bubble icon in your system tray")
    ttk.Label(root, text=f"● done. is running. Look for {where}.", style="Muted.TLabel",
              wraplength=440, justify="left").pack(anchor="w", pady=(2, 12))

    def block(title, en_key, text_key, loud_key, extra=None):
        f = ttk.LabelFrame(root, text=title, padding=14)
        f.pack(fill="x", pady=6)
        ttk.Checkbutton(f, text="Enabled", variable=v[en_key]).grid(row=0, column=0, sticky="w", columnspan=3)
        ttk.Label(f, text="Text").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(f, textvariable=v[text_key], width=36).grid(row=1, column=1, columnspan=2, sticky="we", pady=6)
        ttk.Label(f, text="Sound").grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(f, text="Loud", variable=v[loud_key], value=True).grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(f, text="Silent", variable=v[loud_key], value=False).grid(row=2, column=2, sticky="w")
        if extra:
            extra(f)

    def min_row(f):
        ttk.Label(f, text="Only if longer than").grid(row=3, column=0, sticky="w", pady=(8, 0))
        sb = ttk.Spinbox(f, from_=0, to=3600, increment=30, textvariable=v["min_seconds"], width=6)
        sb.grid(row=3, column=1, sticky="w", pady=(8, 0))
        ttk.Label(f, text="seconds", style="Muted.TLabel").grid(row=3, column=2, sticky="w", pady=(8, 0))

    block("When Claude finishes", "notify_answered", "text_answered", "loud_answered", min_row)
    block("When Claude asks for approval", "notify_approval", "text_approval", "loud_approval")

    g = ttk.LabelFrame(root, text="Watch", padding=14)
    g.pack(fill="x", pady=6)
    ttk.Checkbutton(g, text="Claude desktop app", variable=v["watch_app"]).pack(anchor="w")
    ttk.Checkbutton(g, text="claude.ai in your browser", variable=v["watch_web"]).pack(anchor="w")
    ttk.Checkbutton(g, text="Start done. when I log in", variable=v["autostart"]).pack(anchor="w", pady=(8, 0))

    def save():
        c = core.load()
        for k, var in v.items():
            val = var.get()
            if k == "min_seconds":
                try:
                    val = max(0, int(float(val)))
                except ValueError:
                    val = 0
            elif k.startswith("loud_"):
                val = val in (True, "1", "True", 1)
            c[k] = val
        core.save(c)
        core.set_autostart(c["autostart"])
        root.destroy()

    b = ttk.Frame(root)
    b.pack(fill="x", pady=(14, 0))
    ttk.Button(b, text="Save", style="Accent.TButton", command=save).pack(side="right")
    ttk.Button(b, text="Cancel", command=root.destroy).pack(side="right", padx=8)
    ttk.Button(b, text="Pair phone…", command=lambda: core.open_window("pair")).pack(side="left")

    def quit_all():
        core.quit_running()
        root.destroy()

    ttk.Button(b, text="Quit done.", command=quit_all).pack(side="left", padx=8)
    root.mainloop()


def run(kind):
    (pair_window if kind == "pair" else settings_window)()
