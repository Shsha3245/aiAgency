from ..data_io import read_data_file
from ..llama_integration import analyze_department


def stock_report() -> dict:
    stock = read_data_file("stock.csv")
    critical = stock[stock["Adet"] <= stock["Kritik Seviye"]]
    minimum = stock[stock["Adet"] <= stock["Minimum Seviye"]]
    faulty = stock[stock["Kayip/Hatali"] > 0]
    counts = read_data_file("inventory_counts.csv")
    differences = counts[counts["Sistem Adet"] != counts["Fiziksel Adet"]]
    metrics = {
        "kritik_stoklar": critical["SKU"].tolist(),
        "minimum_altindaki_stoklar": minimum["SKU"].tolist(),
        "kayip_hatali_stoklar": faulty["SKU"].tolist(),
        "stok_degeri": round((stock["Adet"] * stock["Birim Maliyet"]).sum(), 2),
        "son_stok_sayim_tarihi": counts["Sayim Tarihi"].max(),
        "fiziksel_sistem_farki_olan_sku_sayisi": int(len(differences)),
        "fiziksel_sistem_farklari": differences[
            ["SKU", "Sistem Adet", "Fiziksel Adet"]
        ].to_dict(orient="records"),
    }
    return analyze_department(
        "Stok ve Depo Yonetimi",
        "Hammadde, yari mamul ve satisa hazir stoklarin seviye ve kayiplarini izler.",
        metrics,
    )
