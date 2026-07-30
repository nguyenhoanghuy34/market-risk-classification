import pandas as pd

from tqdm import tqdm

from ta.trend import MACD

from .config import (
    MACD_FAST,
    MACD_SLOW,
    MACD_SIGNAL,
)


def add_trend(df: pd.DataFrame) -> pd.DataFrame:

    print("Creating Trend Features...")

    pbar = tqdm(total=3, desc="Trend")

    indicator = MACD(
        close=df["close"],
        window_fast=MACD_FAST,
        window_slow=MACD_SLOW,
        window_sign=MACD_SIGNAL,
    )

    df["MACD"] = indicator.macd()
    pbar.update(1)

    df["MACD_signal"] = indicator.macd_signal()
    pbar.update(1)

    df["MACD_hist"] = indicator.macd_diff()
    pbar.update(1)

    pbar.close()

    return df