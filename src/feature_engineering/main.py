from pathlib import Path

import pandas as pd

from src.feature_engineering.pipeline import FeatureEngineering


INPUT_PATH = Path(
    "data/processed/BTCUSDT/BTCUSDT_1m_clean.csv"
)


def main():

    print("=" * 70)
    print("Loading processed data...")
    print("=" * 70)

    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=[
            "open_time",
            "close_time",
        ],
    )

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {df.shape[1]}")
    print()

    df = FeatureEngineering(df)

    print()
    print("=" * 70)
    print("Feature Engineering Finished")
    print("=" * 70)
    print(df.head())


if __name__ == "__main__":
    main()