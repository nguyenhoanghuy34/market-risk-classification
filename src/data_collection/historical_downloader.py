from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from binance.client import Client
from tqdm import tqdm


class HistoricalDownloader:
    def __init__(self):
        self.client = Client()

    def download(
        self,
        symbol: str,
        interval: str,
        start_date: str,
        end_date: str,
        output_dir: str = "data/raw/historical",
    ) -> Path:

        print(f"\nDownloading {symbol} ({interval})...")

        klines = self.client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_date,
            end_str=end_date,
        )

        columns = [
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

        df = pd.DataFrame(klines, columns=columns)

        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

        numeric_cols = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_asset_volume",
            "taker_buy_base_volume",
            "taker_buy_quote_volume",
        ]

        df[numeric_cols] = df[numeric_cols].astype(float)
        df["number_of_trades"] = df["number_of_trades"].astype(int)

        save_dir = Path(output_dir) / symbol
        save_dir.mkdir(parents=True, exist_ok=True)

        output_path = save_dir / f"{symbol}_{interval}.csv"

        df.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")
        print(f"Rows : {len(df):,}")

        return output_path