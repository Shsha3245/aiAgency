import pandas as pd

def format_finance(data):
    # data: dict veya DataFrame
    df = pd.DataFrame(data)
    summary = {
        "En düşük fiyat": df["Fiyat"].min(),
        "En yüksek fiyat": df["Fiyat"].max(),
        "Ortalama fiyat": round(df["Fiyat"].mean(), 2),
        "İndirim etkisi (%)": round(((df["Fiyat"].max() - df["Fiyat"].min()) / df["Fiyat"].min()) * 100, 1)
    }
    return summary

def format_stock(data):
    df = pd.DataFrame(data)
    kritik = df[df["Adet"] <= df["Kritik Seviye"]]
    min_seviye = df[df["Adet"] <= df["Minimum Seviye"]]
    kayip = df[df["Kayıp/Hatalı"] > 0]

    summary = {
        "Kritik ürünler": kritik[["SKU","Ürün Adı","Adet"]].to_dict(orient="records"),
        "Minimum altı ürünler": min_seviye[["SKU","Ürün Adı","Adet"]].to_dict(orient="records"),
        "Kayıp/Hatalı ürünler": kayip[["SKU","Ürün Adı","Kayıp/Hatalı"]].to_dict(orient="records")
    }
    return summary

def format_production(data):
    # data: dict veya DataFrame
    df = pd.DataFrame(data)
    summary = {
        "Zamanında yetişme (%)": round((df["Durum"].value_counts().get("Doğru",0) / len(df)) * 100, 1),
        "Kapasite ortalama (%)": round(df["Kapasite Kullanımı"].mean(), 1),
        "Fire oranı (%)": round((df["Fire"].sum() / df["Üretim"].sum()) * 100, 1) if "Fire" in df else None
    }
    return summary
