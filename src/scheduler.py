import schedule
import time
from src.main import run_reports
from src.scraper import scrape_configured_supplier_prices

def job():
    print("Rapor çalıştırılıyor...")
    run_reports()


def daily_purchase_price_job():
    """Store the daily prices from the approved supplier site list."""
    results = scrape_configured_supplier_prices()
    print(f"Gunluk tedarikci fiyat taramasi tamamlandi: {len(results)} kaynak.")


# Her saat başı çalıştır
schedule.every().hour.do(job)
# Fiyatlar, yalnizca data/purchase_sites.csv dosyasindaki aktif kaynaklardan alinir.
schedule.every().day.at("09:00").do(daily_purchase_price_job)

while True:
    schedule.run_pending()
    time.sleep(1)
