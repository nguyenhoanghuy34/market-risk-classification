from pathlib import Path

from .extract import extract
from .transform import transform
from .load import load


class ETLPipeline:

    def __init__(self):

        self.raw_path = Path(
            "data/raw/historical/BTCUSDT/BTCUSDT_1m.csv"
        )

        self.output_path = Path(
            "data/processed/BTCUSDT/BTCUSDT_1m_clean.csv"
        )

    def run(self):

        print("========== ETL START ==========")

        df = extract(self.raw_path)

        print(f"Extracted: {len(df):,} rows")

        df = transform(df)

        print(f"After Transform: {len(df):,} rows")

        load(df, self.output_path)

        print("========== ETL DONE ==========")