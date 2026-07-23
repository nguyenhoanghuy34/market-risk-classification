from pathlib import Path

import pandas as pd


def extract(csv_path: str | Path) -> pd.DataFrame:
    """
    Read raw CSV from Binance.
    """

    return pd.read_csv(csv_path)