from pathlib import Path
import pandas as pd


def extract(path: str | Path) -> pd.DataFrame:
    """
    Read raw csv.
    """

    return pd.read_csv(path)