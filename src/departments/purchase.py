from datetime import date

from ..data_io import read_data_file, read_optional_data_file
from ..llama_integration import analyze_department


def purchase_report() -> dict:
    purchase = read_data_file("purchase.csv")
    suppliers = read_data_file("purchase_sites.csv")
    history = read_optional_data_file(
        "purchase_price_history.csv",
        ["Tarih", "Malzeme", "Tedarikci", "Fiyat", "Durum"],
    )
    today_prices = history[
        (history["Tarih"] == date.today().isoformat()) & (history["Durum"] == "Basarili")
    ].copy()
    price_comparisons = []
    if not today_prices.empty:
        today_prices["Fiyat"] = today_prices["Fiyat"].astype(float)
        for material, prices in today_prices.groupby("Malzeme"):
            cheapest = prices.loc[prices["Fiyat"].idxmin()]
            price_comparisons.append(
                f"{material}: {cheapest['Tedarikci']} ({cheapest['Fiyat']:.2f} TL)"
            )
    metrics = {
        "tedarikci_sayisi": int(purchase["Tedarikci"].nunique()),
        "bekleyen_tedarik_sayisi": int((purchase["Durum"] != "Teslim Edildi").sum()),
        "en_uzun_teslimat_gunu": int(purchase["Teslimat Gunu"].max()),
        "tahmini_satin_alma_tutari": round(purchase["Tutar"].sum(), 2),
        "taramaya_tanimli_site_sayisi": int(len(suppliers)),
        "aktif_fiyat_takip_sitesi": int(suppliers["Aktif"].sum()),
        "alternatif_tedarikci_sayisi": int(
            suppliers.groupby("Malzeme")["Tedarikci"].nunique().gt(1).sum()
        ),
        "ortalama_kalite_puani": round(suppliers["Kalite Puani"].mean(), 1),
        "ortalama_teslimat_gunu": round(suppliers["Teslimat Gunu"].mean(), 1),
        "bugun_fiyati_alinan_kaynak_sayisi": int(len(today_prices)),
        "bugunun_en_uygun_fiyatlari": price_comparisons,
    }
    return analyze_department(
        "Satin Alma ve Tedarik",
        "Tedarikci, teslimat, fiyat, kalite, alternatif kaynak ve ihtiyac "
        "planlamasini yonetir. Gunluk taranan fiyat varsa en uygun tedarikciyi belirt.",
        metrics,
    )
