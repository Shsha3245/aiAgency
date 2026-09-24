from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def read_data_file(filename: str) -> pd.DataFrame:
    """Load a UTF-8 CSV from the project's data directory."""
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Veri dosyasi bulunamadi: {path}")
    return pd.read_csv(path)


def read_optional_data_file(filename: str, columns: list[str]) -> pd.DataFrame:
    """Load an optional CSV, returning its expected empty schema when absent."""
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path)
