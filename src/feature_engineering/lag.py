import pandas as pd

from tqdm import tqdm

from .config import LAG_WINDOWS


def add_lag(df: pd.DataFrame) -> pd.DataFrame:

    print("Creating Lag Features...")

    base_columns = [
        "close",
        "volume",
        "RSI_14",
        "MACD",
    ]

    total = len(base_columns) * len(LAG_WINDOWS)

    pbar = tqdm(total=total, desc="Lag")

    for column in base_columns:

        for lag in LAG_WINDOWS:

            df[f"{column}_lag_{lag}"] = (
                df[column]
                .shift(lag)
            )

            pbar.update(1)

    pbar.close()

    return df