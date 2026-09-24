import pandas as pd
from datetime import datetime

def post_to_instagram(file_path, caption):
    # Şimdilik sahte API çağrısı
    print(f"[INSTAGRAM] Paylaşıldı: {file_path} | Açıklama: {caption}")
    return True

def post_to_tiktok(file_path, caption):
    print(f"[TIKTOK] Paylaşıldı: {file_path} | Açıklama: {caption}")
    return True

def post_to_linkedin(file_path, caption):
    print(f"[LINKEDIN] Paylaşıldı: {file_path} | Açıklama: {caption}")
    return True

def run_social_scheduler(csv_path="data/social_posts.csv"):
    df = pd.read_csv(csv_path)
    today = datetime.today().strftime("%Y-%m-%d")

    for _, row in df.iterrows():
        if row["Tarih"] == today:  # sadece bugüne ait gönderileri çalıştır
            platform = row["Platform"].lower()
            file_path = row["Icerik Dosyasi"]
            caption = row["Aciklama"]

            if platform == "instagram":
                post_to_instagram(file_path, caption)
            elif platform == "tiktok":
                post_to_tiktok(file_path, caption)
            elif platform == "linkedin":
                post_to_linkedin(file_path, caption)
            else:
                print(f"[UYARI] Platform desteklenmiyor: {platform}")
