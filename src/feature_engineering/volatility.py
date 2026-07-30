import pandas as pd

from tqdm import tqdm

from ta.volatility import (
    BollingerBands,
    AverageTrueRange,
)

from .config import (
    BB_WINDOWS,
    BB_STD,
    ATR_WINDOWS,
    VOLATILITY_WINDOWS,
)


def add_volatility(df: pd.DataFrame) -> pd.DataFrame:

    total = (
        len(BB_WINDOWS) * 4
        + len(ATR_WINDOWS)
        + len(VOLATILITY_WINDOWS)
    )

    print("Creating Volatility Features...")

    pbar = tqdm(total=total, desc="Volatility")

    # ----------------------------------------
    # Bollinger Bands
    # ----------------------------------------

    for window in BB_WINDOWS:

        bb = BollingerBands(
            close=df["close"],
            window=window,
            window_dev=BB_STD,
        )

        df[f"BB_upper_{window}"] = bb.bollinger_hband()
        pbar.update(1)

        df[f"BB_middle_{window}"] = bb.bollinger_mavg()
        pbar.update(1)

        df[f"BB_lower_{window}"] = bb.bollinger_lband()
        pbar.update(1)

        df[f"BB_width_{window}"] = bb.bollinger_wband()
        pbar.update(1)

    # ----------------------------------------
    # ATR
    # ----------------------------------------

    for window in ATR_WINDOWS:

        atr = AverageTrueRange(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=window,
        )

        df[f"ATR_{window}"] = atr.average_true_range()

        pbar.update(1)

    # ----------------------------------------
    # Rolling Volatility
    # ----------------------------------------

    returns = df["close"].pct_change()

    for window in VOLATILITY_WINDOWS:

        df[f"Volatility_{window}"] = (
            returns
            .rolling(window)
            .std()
        )

        pbar.update(1)

    pbar.close()

    return df