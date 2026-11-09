#!/bin/bash
# Build local de done.app (pour tester). Les versions publiques sont construites par GitHub Actions.
# Usage : bash app/build_mac.sh
set -e
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q pyinstaller pystray pillow qrcode pyobjc-framework-ApplicationServices pyobjc-framework-Cocoa

# Icône .icns à partir du PNG du site
mkdir -p build/done.iconset
for s in 16 32 64 128 256 512; do
  sips -z $s $s ../public/icon-512.png --out build/done.iconset/icon_${s}x${s}.png >/dev/null
  sips -z $((s*2)) $((s*2)) ../public/icon-512.png --out build/done.iconset/icon_${s}x${s}@2x.png >/dev/null
done
iconutil -c icns build/done.iconset -o build/done.icns

rm -rf dist
pyinstaller --noconfirm --windowed --name done --osx-bundle-identifier app.done \
  --icon build/done.icns --collect-submodules done --log-level WARN run.py

# App de barre de menus (pas d'icône dans le Dock) + signature ad hoc
plutil -insert LSUIElement -bool true dist/done.app/Contents/Info.plist
plutil -replace CFBundleShortVersionString -string 0.1.0 dist/done.app/Contents/Info.plist
codesign --force --deep -s - dist/done.app

ditto -c -k --keepParent dist/done.app dist/done-mac.zip
echo "OK -> app/dist/done.app (+ dist/done-mac.zip)"
