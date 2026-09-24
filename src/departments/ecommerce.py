from ..data_io import read_data_file
from ..llama_integration import analyze_department


def ecommerce_report() -> dict:
    """Summarize the operational e-commerce metrics required by the document."""
    products = read_data_file("ecommerce_products.csv")
    funnel = read_data_file("ecommerce_funnel.csv")
    performance = read_data_file("ecommerce_product_performance.csv")
    metrics = {
        "aktif_urun_sayisi": int((products["Yayinda"] == True).sum()),
        "stokta_tukenen_urunler": products.loc[products["Stok"] == 0, "Urun"].tolist(),
        "dusuk_donusumlu_urunler": products.loc[
            (products["Goruntulenme"] >= 100) & (products["Donusum Orani"] < 1),
            "Urun",
        ].tolist(),
        "ortalama_donusum_orani": round(products["Donusum Orani"].mean(), 2),
        "sepete_ekleme_orani": round(
            funnel["Sepete Ekleme"].sum() / funnel["Oturum"].sum() * 100, 2
        ),
        "sepetten_siparise_donusum_orani": round(
            funnel["Siparis"].sum() / funnel["Sepete Ekleme"].sum() * 100, 2
        ),
        "odeme_basarisizlik_sayisi": int(funnel["Odeme Basarisiz"].sum()),
        "en_cok_satan_urun": performance.loc[
            performance["Satilan Adet"].idxmax(), "Urun"
        ],
        "dusuk_satan_urunler": performance.loc[
            performance["Satilan Adet"] <= performance["Satilan Adet"].median(), "Urun"
        ].tolist(),
    }
    return analyze_department(
        "E-ticaret ve Dijital Operasyonlar",
        "Urun yayini, stok, sepet, odeme, goruntulenme, en cok ve dusuk satan urun "
        "ile donusum performansini yonetir.",
        metrics,
    )
