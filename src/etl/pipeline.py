from pathlib import Path

from .extract import extract
from .transform import transform
from .load import load


RAW_PATH = Path(
    "data/raw/historical/BTCUSDT/BTCUSDT_1m.csv"
)

OUTPUT_PATH = Path(
    "data/processed/BTCUSDT/BTCUSDT_1m_clean.csv"
)


def ETL():

    df = extract(RAW_PATH)

    df = transform(df)

    load(
        df,
        OUTPUT_PATH,
    )

    print("=" * 60)

    print("ETL Finished")

    print(df.shape)

    print(f"Saved -> {OUTPUT_PATH}")

    return df


if __name__ == "__main__":

    ETL()