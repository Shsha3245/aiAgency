from . import finance, marketing, production, purchase, sales, stock
from .ecommerce import ecommerce_report
from .research_and_development import research_and_development_report
from ..llama_integration import run_llama


def executive_summary() -> dict:
    """Combine department reports for the CEO's cross-functional review."""
    reports = {
        "finans": finance.monthly_report(),
        "satin_alma": purchase.purchase_report(),
        "stok": stock.stock_report(),
        "uretim": production.production_report(),
        "ar_ge": research_and_development_report(),
        "satis": sales.sales_report(),
        "pazarlama": marketing.marketing_report(),
        "e_ticaret": ecommerce_report(),
    }
    reports["yonetim_uyarilari"] = [
        f"Kritik stok: {', '.join(reports['stok']['metrikler']['kritik_stoklar']) or 'yok'}",
        f"Bekleyen siparis: {reports['satis']['metrikler']['bekleyen_siparisler']}",
        f"Geciken uretim isi: {reports['uretim']['metrikler']['geciken_is_sayisi']}",
        "Stokta tukenen e-ticaret urunu: "
        f"{', '.join(reports['e_ticaret']['metrikler']['stokta_tukenen_urunler']) or 'yok'}",
    ]
    reports["ceo_yapay_zeka_ozeti"] = run_llama(
        f"""Sen Elaia Ceramics CEO'suna rapor veren bir genel yonetim asistanisin.
Asagidaki departman verileri ve analizlerinden yararlanarak Turkce, kisa bir
yonetici ozeti yaz. En fazla 5 madde kullan. Once kritik karar ve riskleri,
sonra departmanlar arasi uygulanabilir aksiyonlari belirt. Veri uydurma.

{reports}"""
    )
    return reports
