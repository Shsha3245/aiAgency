#!/usr/bin/env bash

# Hata durumunda çalışmayı durdur
set -e

echo "=================================================="
echo "       Elaia Ceramics macOS App Derlemesi         "
echo "=================================================="

# 1. Sanal ortam varsa aktif et (PyInstaller ve paketlerin bulunması için)
if [ -d "venv" ]; then
    echo "--> Sanal ortam (venv) aktif ediliyor..."
    source venv/bin/activate
fi

# Her ihtimale karşı sistem Python bin klasörlerini PATH'e ekle
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# 2. Gerekli paketlerin yüklü olduğundan emin ol
pip install --upgrade pip
pip install -r requirements.txt

# 3. PyInstaller ile .app paketini derle
echo "--> Uygulama derleniyor..."
pyinstaller --noconfirm --onedir --windowed \
    --name "Elaia Ceramics" \
    --add-data "data:data" \
    ui/desktop_app.py

echo ""
echo "=================================================="
echo " Derleme Tamamlandı! Uygulama: dist/Elaia Ceramics.app"
echo "=================================================="
