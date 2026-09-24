from ..data_io import read_data_file
from ..llama_integration import analyze_department


def production_report() -> dict:
    production = read_data_file("production.csv")
    stages = read_data_file("production_stages.csv")
    kiln = read_data_file("kiln_capacity.csv")
    metrics = {
        "zamaninda_teslim_orani": round(
            (production["Durum"] == "Zamaninda").mean() * 100, 1
        ),
        "ortalama_kapasite_kullanimi": round(
            production["Kapasite Kullanimi"].mean(), 1
        ),
        "fire_orani": round(
            production["Fire"].sum() / production["Planlanan Adet"].sum() * 100, 1
        ),
        "geciken_is_sayisi": int((production["Durum"] == "Gecikti").sum()),
        "uretim_asamalari_durumu": stages["Asama"].value_counts().to_dict(),
        "bekleyen_uretim_asamasi_sayisi": int((stages["Durum"] != "Tamamlandi").sum()),
        "firin_kapasite_kullanimi": round(kiln["Kapasite Kullanimi"].mean(), 1),
        "firin_bos_kapasite": round((100 - kiln["Kapasite Kullanimi"]).mean(), 1),
    }
    return analyze_department(
        "Uretim ve Uretim Planlama",
        "Termin, uretim asamalari, firin kapasitesi, kapasite kullanimi ve fireyi takip eder.",
        metrics,
    )
