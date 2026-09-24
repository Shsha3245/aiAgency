import csv
from pathlib import Path

DATA_FILE = Path("data/prices.csv")

def save_prices(results):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(results)
