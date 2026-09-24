import json
import sys

from src.departments.management import executive_summary


def _json_default(value):
    """Convert scalar values returned by pandas aggregations for JSON output."""
    if hasattr(value, "item"):
        return value.item()
    raise TypeError(f"{type(value).__name__} is not JSON serializable")


def run_reports() -> dict:
    """Generate and display the CEO report across all defined departments."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    summary = executive_summary()
    print("=== Elaia Ceramics Yonetici Ozeti ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=_json_default))
    return summary


if __name__ == "__main__":
    run_reports()
