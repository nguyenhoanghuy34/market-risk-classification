import pandas as pd


def add_time_feature(df: pd.DataFrame) -> pd.DataFrame:

    print("Creating Time Features...")

    df["hour"] = df["open_time"].dt.hour

    df["minute"] = df["open_time"].dt.minute

    df["day"] = df["open_time"].dt.day

    df["month"] = df["open_time"].dt.month

    df["day_of_week"] = df["open_time"].dt.dayofweek

    df["week_of_year"] = (
        df["open_time"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    return df