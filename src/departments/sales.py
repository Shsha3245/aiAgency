from ..data_io import read_data_file
from ..llama_integration import analyze_department


def sales_report() -> dict:
    sales = read_data_file("sales.csv")
    prospects = read_data_file("sales_prospects.csv")
    reorders = read_data_file("reorder_schedule.csv")
    by_customer = sales.groupby("Musteri Tipi")["Tutar"].sum()
    by_product = sales.groupby("Urun")["Tutar"].sum()
    metrics = {
        "toplam_satis": round(sales["Tutar"].sum(), 2),
        "siparis_sayisi": int(len(sales)),
        "en_cok_gelir_getiren_urun": by_product.idxmax(),
        "en_degerli_musteri_grubu": by_customer.idxmax(),
        "bekleyen_siparisler": int((sales["Durum"] != "Tamamlandi").sum()),
        "kurumsal_musteri_havuzu": int(
            (prospects["Musteri Tipi"] == "Kurumsal").sum()
        ),
        "toplam_potansiyel_teklif_tutari": round(prospects["Potansiyel Tutar"].sum(), 2),
        "bu_ay_yeniden_siparis_beklenen_musteri_sayisi": int(
            (reorders["Durum"] == "Bu Ay Bekleniyor").sum()
        ),
        "gecikmis_yeniden_siparis_sayisi": int(
            (reorders["Durum"] == "Gecikti").sum()
        ),
    }
    return analyze_department(
        "Satis ve Is Gelistirme",
        "Perakende ve B2B satislari, siparisleri, kurumsal musteri havuzunu ve "
        "yeniden siparis firsatlarini yonetir.",
        metrics,
    )
