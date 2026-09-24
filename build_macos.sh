#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -r requirements.txt
pyinstaller --noconfirm --windowed --name "Elaia Ceramics" --paths . ui/desktop_app.py
echo "macOS uygulamasi hazir: dist/Elaia Ceramics.app"
