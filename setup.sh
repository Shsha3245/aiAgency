#!/usr/bin/env bash

# Hata durumunda çalışmayı durdur
set -e

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "=================================================="
echo "   Elaia Ceramics / aiAgency macOS Kurulumu      "
echo "=================================================="

# 1. Homebrew Kurulumu
if ! command -v brew &> /dev/null; then
    echo "--> [1/5] Homebrew bulunamadı, kuruluyor..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Apple Silicon (M1/M2/M3) ve Intel Mac PATH ayarı
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -f "/usr/local/bin/brew" ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    echo "--> [1/5] Homebrew zaten kurulu."
fi

# 2. Python, Git ve Ollama Kurulumu
echo "--> [2/5] Python, Git ve Ollama yükleniyor..."
brew update
brew install python git ollama

# 3. Ollama Servisi ve Model İndirme
echo "--> [3/5] Ollama servisi başlatılıyor ve llama3.2:3b modeli indiriliyor..."
brew services start ollama

# Servisin başlaması için 2 saniye bekle
sleep 2
ollama pull llama3.2:3b

# 4. Python Sanal Ortam (venv) Kurulumu ve Bağımlılıklar
echo "--> [4/5] Python sanal ortamı (venv) oluşturuluyor ve paketler yükleniyor..."
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "UYARI: requirements.txt bulunamadı!"
fi

# 5. İzinlerin Ayarlanması
echo "--> [5/5] macOS derleme scripti izinleri düzenleniyor..."
if [ -f "build_macos.sh" ]; then
    chmod +x build_macos.sh
fi

echo ""
echo "=================================================="
echo "            Kurulum Başarıyla Tamamlandı!         "
echo "=================================================="
echo ""
echo "Uygulamayı hemen test etmek için:"
echo "    source venv/bin/activate"
echo "    python3 -m ui.desktop_app"
echo ""
echo "Mac .app paketini üretmek için:"
echo "    ./build_macos.sh"
echo "=================================================="
