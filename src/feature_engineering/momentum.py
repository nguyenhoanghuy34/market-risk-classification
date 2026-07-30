import pandas as pd

from tqdm import tqdm

from ta.momentum import RSIIndicator
from ta.momentum import ROCIndicator

from .config import RSI_WINDOWS
from .config import ROC_WINDOWS
from .config import MOMENTUM_WINDOWS


def add_momentum(df: pd.DataFrame) -> pd.DataFrame:

    print("Creating Momentum Features...")

    total = (
        len(RSI_WINDOWS)
        + len(ROC_WINDOWS)
        + len(MOMENTUM_WINDOWS)
    )

    pbar = tqdm(
        total=total,
        desc="Momentum",
    )

    # -----------------------------------
    # RSI
    # -----------------------------------

    for window in RSI_WINDOWS:

        df[f"RSI_{window}"] = (
            RSIIndicator(
                close=df["close"],
                window=window,
            )
            .rsi()
        )

        pbar.update(1)

    # -----------------------------------
    # ROC
    # -----------------------------------

    for window in ROC_WINDOWS:

        df[f"ROC_{window}"] = (
            ROCIndicator(
                close=df["close"],
                window=window,
            )
            .roc()
        )

        pbar.update(1)

    # -----------------------------------
    # Momentum
    # -----------------------------------

    for window in MOMENTUM_WINDOWS:

        df[f"Momentum_{window}"] = (
            df["close"]
            - df["close"].shift(window)
        )

        pbar.update(1)

    pbar.close()

    return df