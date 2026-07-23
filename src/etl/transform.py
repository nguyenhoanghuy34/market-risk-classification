import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate Binance historical data.
    """

    df = df.copy()

    # --------------------------
    # Convert datetime
    # --------------------------

    df["open_time"] = pd.to_datetime(df["open_time"])
    df["close_time"] = pd.to_datetime(df["close_time"])

    # --------------------------
    # Convert numeric columns
    # --------------------------

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_asset_volume",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
    ]

    df[numeric_columns] = df[numeric_columns].astype(float)

    df["number_of_trades"] = df["number_of_trades"].astype(int)

    # --------------------------
    # Sort
    # --------------------------

    df = df.sort_values("open_time")

    # --------------------------
    # Remove duplicates
    # --------------------------

    df = df.drop_duplicates(subset="open_time")

    # --------------------------
    # Remove missing values
    # --------------------------

    df = df.dropna()

    # --------------------------
    # Basic validation
    # --------------------------

    df = df[df["high"] >= df["low"]]

    df = df[df["volume"] >= 0]

    df = df[df["open"] > 0]

    df = df[df["close"] > 0]

    df = df[df["close_time"] > df["open_time"]]

    # --------------------------
    # Reset index
    # --------------------------

    df = df.reset_index(drop=True)

    return df