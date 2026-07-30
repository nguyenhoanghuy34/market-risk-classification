import pandas as pd
from tqdm import tqdm

from .config import SMA_WINDOWS
from .config import EMA_WINDOWS


def add_moving_average(df: pd.DataFrame) -> pd.DataFrame:

    print("Creating Moving Average Features...")

    windows = SMA_WINDOWS + EMA_WINDOWS

    pbar = tqdm(
        total=len(windows),
        desc="Moving Average",
    )

    # -------------------------
    # SMA
    # -------------------------

    for window in SMA_WINDOWS:

        df[f"SMA_{window}"] = (
            df["close"]
            .rolling(window)
            .mean()
        )

        pbar.update(1)

    # -------------------------
    # EMA
    # -------------------------

    for window in EMA_WINDOWS:

        df[f"EMA_{window}"] = (
            df["close"]
            .ewm(
                span=window,
                adjust=False,
            )
            .mean()
        )

        pbar.update(1)

    pbar.close()

    return df