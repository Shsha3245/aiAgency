from ..data_io import read_data_file
from ..llama_integration import analyze_department


def marketing_report() -> dict:
    posts = read_data_file("social_posts.csv")
    competitors = read_data_file("marketing_competitor_analysis.csv")
    brand_audits = read_data_file("brand_consistency_audits.csv")
    metrics = {
        "planli_icerik_sayisi": int(len(posts)),
        "platform_sayisi": int(posts["Platform"].nunique()),
        "kampanya_icerigi_sayisi": int(posts["Kampanya"].notna().sum()),
        "toplam_erisim": int(posts["Erisim"].sum()),
        "ortalama_etkilesim_orani": round(posts["Etkilesim Orani"].mean(), 2),
        "rakip_analizi_sayisi": int(len(competitors)),
        "son_rakip_bulgulari": competitors.sort_values("Tarih", ascending=False)
        .head(3)["Bulgu"].tolist(),
        "marka_dili_tutarlilik_orani": round(
            (brand_audits["Durum"] == "Uygun").mean() * 100, 1
        ),
        "marka_dili_iyilestirme_alani": brand_audits.loc[
            brand_audits["Durum"] != "Uygun", "Alan"
        ].tolist(),
    }
    return analyze_department(
        "Pazarlama ve Marka Yonetimi",
        "Marka, kampanya, hedef kitle, rakip analizi, marka dili tutarliligi ve "
        "pazarlama performansini yonetir.",
        metrics,
    )
