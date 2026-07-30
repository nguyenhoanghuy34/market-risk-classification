import pandas as pd

from tqdm import tqdm

from .config import (
    RETURN_WINDOWS,
    ROLLING_PRICE_WINDOWS,
)


def add_price_action(df: pd.DataFrame) -> pd.DataFrame:

    print("Creating Price Action Features...")

    total = (
        len(RETURN_WINDOWS) * 2
        + len(ROLLING_PRICE_WINDOWS) * 2
    )

    pbar = tqdm(total=total, desc="Price Action")

    # ----------------------------------
    # Return
    # ----------------------------------

    for window in RETURN_WINDOWS:

        df[f"Return_{window}"] = (
            df["close"]
            .pct_change(window)
        )

        pbar.update(1)

        df[f"Log_Return_{window}"] = (
            (df["close"] / df["close"].shift(window))
            .apply(lambda x: None if pd.isna(x) else __import__("numpy").log(x))
        )

        pbar.update(1)

    # ----------------------------------
    # Rolling Mean / Std
    # ----------------------------------

    for window in ROLLING_PRICE_WINDOWS:

        df[f"Rolling_Mean_{window}"] = (
            df["close"]
            .rolling(window)
            .mean()
        )

        pbar.update(1)

        df[f"Rolling_STD_{window}"] = (
            df["close"]
            .rolling(window)
            .std()
        )

        pbar.update(1)

    pbar.close()

    return df