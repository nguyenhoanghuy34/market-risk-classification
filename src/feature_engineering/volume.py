import pandas as pd

from tqdm import tqdm

from ta.volume import (
    OnBalanceVolumeIndicator,
    VolumeWeightedAveragePrice,
)

from .config import VOLUME_MA_WINDOWS


def add_volume(df: pd.DataFrame) -> pd.DataFrame:

    print("Creating Volume Features...")

    total = 2 + len(VOLUME_MA_WINDOWS)

    pbar = tqdm(total=total, desc="Volume")

    # ---------------------------
    # OBV
    # ---------------------------

    obv = OnBalanceVolumeIndicator(
        close=df["close"],
        volume=df["volume"],
    )

    df["OBV"] = obv.on_balance_volume()

    pbar.update(1)

    # ---------------------------
    # VWAP
    # ---------------------------

    vwap = VolumeWeightedAveragePrice(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        volume=df["volume"],
    )

    df["VWAP"] = vwap.volume_weighted_average_price()

    pbar.update(1)

    # ---------------------------
    # Volume Moving Average
    # ---------------------------

    for window in VOLUME_MA_WINDOWS:

        df[f"Volume_MA_{window}"] = (
            df["volume"]
            .rolling(window)
            .mean()
        )

        pbar.update(1)

    pbar.close()

    return df