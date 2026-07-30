from pathlib import Path
from time import perf_counter

import pandas as pd
from tqdm import tqdm

from .config import (
    OUTPUT_FOLDER,
    OUTPUT_FILE,
)

from .moving_average import add_moving_average
from .momentum import add_momentum
from .trend import add_trend
from .volatility import add_volatility
from .volume import add_volume
from .price_action import add_price_action
from .time_feature import add_time_feature
from .lag import add_lag


class FeatureEngineeringPipeline:

    def __init__(self):

        self.steps = [
            ("Moving Average", add_moving_average),
            ("Momentum", add_momentum),
            ("Trend", add_trend),
            ("Volatility", add_volatility),
            ("Volume", add_volume),
            ("Price Action", add_price_action),
            ("Time Feature", add_time_feature),
            ("Lag", add_lag),
        ]

    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        start = perf_counter()

        print("=" * 70)
        print("FEATURE ENGINEERING")
        print("=" * 70)

        pbar = tqdm(
            self.steps,
            desc="Pipeline",
        )

        for _, func in pbar:

            pbar.set_postfix(
                step=func.__name__,
            )

            df = func(df)

        print()

        print("Removing NaN...")

        before = len(df)

        df = df.dropna()

        removed = before - len(df)

        print(f"Removed {removed:,} rows")

        df = df.reset_index(drop=True)

        elapsed = perf_counter() - start

        print()

        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)

        print(f"Rows      : {len(df):,}")
        print(f"Columns   : {df.shape[1]}")
        print(f"Time      : {elapsed:.2f} sec")

        return df

    def save(
        self,
        df: pd.DataFrame,
    ):

        output_dir = Path(OUTPUT_FOLDER)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = output_dir / OUTPUT_FILE

        print()

        print("Saving Feature Store...")

        df.to_parquet(
            output_path,
            index=False,
        )

        print(f"Saved -> {output_path}")


def FeatureEngineering(
    df: pd.DataFrame,
) -> pd.DataFrame:

    pipeline = FeatureEngineeringPipeline()

    df = pipeline.transform(df)

    pipeline.save(df)

    return df