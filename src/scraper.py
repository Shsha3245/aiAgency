import csv
import re
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .data_io import DATA_DIR, read_data_file


PRICE_HISTORY_FILE = DATA_DIR / "purchase_price_history.csv"
REQUEST_TIMEOUT_SECONDS = 20
USER_AGENT = "ElaiaCeramicsPriceMonitor/1.0 (+local purchasing analysis)"


def get_price(url: str, selector: str) -> str | None:
    """Read a price element from a supplier page."""
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    element = BeautifulSoup(response.text, "html.parser").select_one(selector)
    return element.get_text(" ", strip=True) if element else None


def parse_price(price_text: str) -> float:
    """Convert common Turkish price strings such as '1.249,90 TL' to a number."""
    normalized = re.sub(r"[^\d,.-]", "", price_text).strip()
    if not normalized:
        raise ValueError("Fiyat metninde sayisal deger bulunamadi.")
    if "," in normalized and "." in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    elif "," in normalized:
        normalized = normalized.replace(",", ".")
    return float(normalized)


def append_price_history(results: list[dict]) -> None:
    """Persist successful daily supplier-price snapshots for trend comparisons."""
    if not results:
        return
    PRICE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_header = not PRICE_HISTORY_FILE.exists() or PRICE_HISTORY_FILE.stat().st_size == 0
    with PRICE_HISTORY_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(results)


def scrape_configured_supplier_prices() -> pd.DataFrame:
    """Scrape enabled supplier pages and save successful prices with today's date."""
    suppliers = read_data_file("purchase_sites.csv")
    active_suppliers = suppliers[suppliers["Aktif"] == True]
    results = []

    for _, supplier in active_suppliers.iterrows():
        checked_at = datetime.now().isoformat(timespec="seconds")
        try:
            raw_price = get_price(supplier["URL"], supplier["CSS Secici"])
            if raw_price is None:
                raise ValueError("CSS secicisiyle fiyat alani bulunamadi.")
            results.append(
                {
                    "Tarih": date.today().isoformat(),
                    "Kontrol Zamani": checked_at,
                    "Malzeme": supplier["Malzeme"],
                    "Tedarikci": supplier["Tedarikci"],
                    "URL": supplier["URL"],
                    "Fiyat": parse_price(raw_price),
                    "Para Birimi": supplier["Para Birimi"],
                    "Durum": "Basarili",
                    "Hata": "",
                }
            )
        except (requests.RequestException, ValueError) as error:
            results.append(
                {
                    "Tarih": date.today().isoformat(),
                    "Kontrol Zamani": checked_at,
                    "Malzeme": supplier["Malzeme"],
                    "Tedarikci": supplier["Tedarikci"],
                    "URL": supplier["URL"],
                    "Fiyat": "",
                    "Para Birimi": supplier["Para Birimi"],
                    "Durum": "Basarisiz",
                    "Hata": str(error),
                }
            )

    successful_results = [result for result in results if result["Durum"] == "Basarili"]
    append_price_history(successful_results)
    return pd.DataFrame(results)
