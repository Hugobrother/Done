import sys

if __name__ == "__main__" or getattr(sys, "frozen", False):
    if "--check-ax" in sys.argv:
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
