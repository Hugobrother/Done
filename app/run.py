# Point d'entrée de l'exécutable (PyInstaller).
# Imports explicites : PyInstaller ne voit que ce qui est importé "en dur".
import sys

from done import core  # noqa: F401  (force l'inclusion du paquet)

if "--version" in sys.argv:
    import os, certifi
    ok = os.path.exists(certifi.where())
    print("done. 0.1 | certificates:", "ok" if ok else "MISSING")
    sys.exit(0 if ok else 1)

if "--check-ax" in sys.argv:
    # Process neuf : macOS donne la vraie valeur de la permission (pas celle mise en cache)
    if sys.platform == "darwin":
        from ApplicationServices import AXIsProcessTrusted
        sys.exit(0 if AXIsProcessTrusted() else 1)
    sys.exit(0)

if "--ui" in sys.argv:
    from done import ui
    ui.run(sys.argv[sys.argv.index("--ui") + 1])
else:
    from done import app
    app.main()
