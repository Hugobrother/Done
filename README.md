# done.

Pings your phone when Claude finishes answering, or when it asks for approval.
Watches the Claude desktop app (Mac, Windows) and claude.ai in your browser (Mac, Windows, Linux).
Notifications go **computer → ntfy.sh → phone** (free ntfy app on iPhone / Android).

## Structure
| Path | What |
|---|---|
| `app/` | Desktop app (Python): tray menu, detection, settings, pairing QR |
| `public/` | Static website on Firebase Hosting: landing page + `pair.html` (opened by the QR code) |
| `.github/workflows/build.yml` | Builds Mac / Windows / Linux and publishes a GitHub Release |

No backend: Firebase only serves static pages (free tier). Downloads are served by GitHub Releases.

## Dev (Mac)
```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install pystray pillow qrcode pyobjc-framework-ApplicationServices pyobjc-framework-Cocoa
python3 -m done
```
Windows: `pip install pystray pillow qrcode uiautomation psutil`
Linux: `pip install pystray pillow qrcode "PyGObject<3.51" python-xlib` (+ `gir1.2-atspi-2.0`)

## Release
```bash
git tag v0.1.1
git push origin v0.1.1
```
GitHub Actions builds `done-mac.zip`, `done-windows.exe`, `done-linux` and attaches them to the release.
The website links to `releases/latest/download/...`, so it updates by itself.

## Website
```bash
firebase deploy --only hosting
```
