from ..data_io import read_data_file
from ..llama_integration import analyze_department


def monthly_report() -> dict:
    """Create the finance summary defined in the department responsibility document."""
    sales = read_data_file("sales.csv")
    expenses = read_data_file("expenses.csv")
    revenue = sales["Tutar"].sum()
    total_expense = expenses["Tutar"].sum()
    profit = revenue - total_expense
    largest_expense = expenses.loc[expenses["Tutar"].idxmax()]
    metrics = {
        "gelir": round(revenue, 2),
        "gider": round(total_expense, 2),
        "kar_zarar": round(profit, 2),
        "nakit_akisi": round(profit, 2),
        "en_buyuk_gider": largest_expense["Kalem"],
        "en_buyuk_gider_tutari": round(largest_expense["Tutar"], 2),
        "en_buyuk_giderin_toplam_gidere_orani": round(
            largest_expense["Tutar"] / total_expense * 100, 1
        ),
    }
    return analyze_department(
        "Finans ve Muhasebe",
        "Gelir-gider, kar-zarar, nakit akisi ve maliyetleri takip eder.",
        metrics,
    )
