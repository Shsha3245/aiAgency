from ..data_io import read_data_file
from ..llama_integration import analyze_department


def research_and_development_report() -> dict:
    """Report prototype status, cost and production feasibility."""
    projects = read_data_file("research_and_development.csv")
    research = read_data_file("research_trends.csv")
    ready = projects[projects["Durum"] == "Onay Bekliyor"]
    metrics = {
        "aktif_prototip_sayisi": int((projects["Durum"] == "Gelistiriliyor").sum()),
        "onay_bekleyen_koleksiyonlar": ready["Proje"].tolist(),
        "ortalama_tahmini_maliyet": round(projects["Tahmini Maliyet"].mean(), 2),
        "uretilebilir_proje_sayisi": int(projects["Uretilebilir"].sum()),
        "rakip_ve_trend_arastirmasi_sayisi": int(
            (research["Kategori"] == "Rakip/Trend").sum()
        ),
        "sir_ve_kil_arastirmasi_sayisi": int(
            (research["Kategori"] == "Sir/Kil").sum()
        ),
        "son_arastirma_konulari": research.sort_values("Tarih", ascending=False)
        .head(3)["Konu"].tolist(),
    }
    return analyze_department(
        "AR-GE ve Urun Gelistirme",
        "Prototipleri, yeni koleksiyonlari, rakip ve trendleri, sir/kil arastirmalarini, "
        "maliyetleri ve uretilebilirligi degerlendirir.",
        metrics,
    )
