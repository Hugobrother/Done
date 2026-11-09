import sys

if __name__ == "__main__" or getattr(sys, "frozen", False):
    if "--ui" in sys.argv:
        from done import ui
        ui.run(sys.argv[sys.argv.index("--ui") + 1])
    else:
        from done import app
        app.main()
