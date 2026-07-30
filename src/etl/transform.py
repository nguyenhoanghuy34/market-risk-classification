import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:

    # -------------------------------
    # Rename columns
    # -------------------------------

    df.columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
        "ignore",
    ]

    # -------------------------------
    # Datetime
    # -------------------------------

    df["open_time"] = pd.to_datetime(
        df["open_time"],
        unit="ms",
    )

    df["close_time"] = pd.to_datetime(
        df["close_time"],
        unit="ms",
    )

    # -------------------------------
    # Numeric
    # -------------------------------

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
    ]

    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    )

    # -------------------------------
    # Remove duplicates
    # -------------------------------

    df = df.drop_duplicates(
        subset="open_time",
    )

    # -------------------------------
    # Sort
    # -------------------------------

    df = df.sort_values(
        "open_time",
    )

    # -------------------------------
    # Remove NaN
    # -------------------------------

    df = df.dropna()

    # -------------------------------
    # Remove impossible rows
    # -------------------------------

    df = df[df["volume"] >= 0]

    df = df[df["high"] >= df["low"]]

    df = df[df["high"] >= df["open"]]

    df = df[df["high"] >= df["close"]]

    df = df[df["low"] <= df["open"]]

    df = df[df["low"] <= df["close"]]

    # -------------------------------
    # Reset index
    # -------------------------------

    df = df.reset_index(drop=True)

    return df