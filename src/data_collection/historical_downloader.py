from pathlib import Path

import csv
import time
import requests
from tqdm import tqdm


# =====================================================
# Config
# =====================================================

SYMBOL = "BTCUSDT"
INTERVAL = "1m"

LIMIT = 1000
TARGET_ROWS = 2_000_000

BASE_URL = "https://api.binance.com/api/v3/klines"

OUTPUT_DIR = Path("data/raw/historical") / SYMBOL
OUTPUT_FILE = OUTPUT_DIR / f"{SYMBOL}_{INTERVAL}.csv"


# =====================================================
# Create folder
# =====================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# CSV Header
# =====================================================

HEADER = [
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


# =====================================================
# Downloader
# =====================================================

def download():

    start_time = 0

    total = 0

    first_write = not OUTPUT_FILE.exists()

    with open(
        OUTPUT_FILE,
        "a",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        if first_write:
            writer.writerow(HEADER)

        pbar = tqdm(
            total=TARGET_ROWS,
            desc="Downloading",
            unit="rows",
        )

        while total < TARGET_ROWS:

            params = {
                "symbol": SYMBOL,
                "interval": INTERVAL,
                "limit": LIMIT,
                "startTime": start_time,
            }

            response = requests.get(BASE_URL, params=params, timeout=30)

            response.raise_for_status()

            data = response.json()

            if len(data) == 0:
                break

            writer.writerows(data)

            batch = len(data)

            total += batch

            pbar.update(batch)

            start_time = data[-1][6] + 1

            time.sleep(0.05)

        pbar.close()

    print("=" * 60)
    print("Finished")
    print(f"Saved : {OUTPUT_FILE}")
    print(f"Rows  : {total:,}")


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":
    download()