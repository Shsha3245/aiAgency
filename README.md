# Elaia Ceramics - Yapay Zeka Destekli Yonetim Sistemi

Bu proje, departman sorumluluk dokumanindaki operasyonlari yonetici ozeti
halinde bir araya getirir. Her departman metrikleri hesaplanir, ardindan yerel
Ollama modeli `llama3.2:3b` ile analiz edilir; CEO ozeti de ayni modelle
uretilir.

## Kapsam

- **Genel Yonetim / CEO:** Departman raporlarini birlestirir ve kritik
  uyari listesini uretir.
- **Finans, Satis, Stok, Uretim, Satin Alma ve Pazarlama:** Gelir-gider,
  siparis, stok esigi, uretim, tedarik ve sosyal-medya metriklerini raporlar.
- **AR-GE:** Prototip durumunu, maliyeti ve uretilebilirligi takip eder.
- **E-ticaret:** Yayin/stok durumu, goruntulenme ve donusum metriklerini
  raporlar.
- **Sosyal medya:** Icerik takvimi `src/social_media.py` araciligiyla
  isletilebilir; gercek platform entegrasyonu eklenene kadar yayini simule eder.

Ornek veri dosyalari `data/` altindadir. Gercek operasyon verileri ayni sutun
adlariyla bu dosyalarin yerine aktarilabilir.

## Gunluk satin alma fiyat taramasi

Fiyat takibi yalnizca `data/purchase_sites.csv` dosyasinda tanimlanan
kaynaklardan yapilir. Rehberdeki sekiz onayli tedarikci ana URL'si dosyaya
eklenmistir. Her satira izlenecek belirli urunun URL'sini ve o urun sayfasindaki
fiyat elementinin CSS secicisini yazin; kullanilacak satirlari `Aktif` alaninda
`True` yapin. Ana sayfalar fiyat izleme icin yeterli olmadigindan kaynaklar,
urun URL'si ve dogrulanmis CSS secicisi girilene kadar pasif kalir.

Guncel taramayi elle calistirmak icin:

```powershell
python -c "from src.scraper import scrape_configured_supplier_prices; print(scrape_configured_supplier_prices())"
```

Basarili fiyatlar `data/purchase_price_history.csv` dosyasina gunluk olarak
kaydedilir. `src/scheduler.py`, her gun saat 09:00'da ayni taramayi calistirir.
Satın Alma raporu, o gun elde edilen fiyatlar arasinda her malzeme icin en
uygun tedarikciyi Ollama analizine aktarir.

## Calistirma

```powershell
python -m src.main
```

Ollama'nin kurulu ve modelin hazir olmasi gerekir:

```powershell
ollama list
```

## Masaustu uygulamasi

Tek kullanicili masaustu arayuzu `ui/desktop_app.py` dosyasindadir. Arayuz,
backend raporlama modullerini degistirmeden kullanir; CSV kaynaklarini tablo
ekraninda duzenlemeyi, Excel iceri aktarmayi/disari aktarmayi ve her departman
icin ayri PDF olusturmayi saglar.

```powershell
python -m pip install -r requirements.txt
python -m ui.desktop_app
```

PDF dosyalari `exports/` klasorune ayri ayri kaydedilir. Bir PDF olusturmak
icin **Departman Raporlari** ekranindan departmani secin, raporu hazirlayin ve
**Bu Departmani PDF Olarak Kaydet** duymesine basin.

### macOS `.app` paketi

macOS uygulamasi macOS makinesinde paketlenmelidir. Projeyi Mac'e kopyalayip
Terminal'de asagidaki komutu calistirin:

```bash
chmod +x build_macos.sh
./build_macos.sh
```

Olusan uygulama `dist/Elaia Ceramics.app` yolunda yer alir. Uygulamanin
Ollama analizleri icin Mac'te Ollama'nin calisiyor ve `llama3.2:3b` modelinin
kurulu olmasi gerekir.
