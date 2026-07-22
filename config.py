from pathlib import Path

# ==========================
# Binance
# ==========================
SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
]

INTERVAL = "1m"

START_DATE = "1 Jan, 2025"
END_DATE = "15 Jan, 2025"

# ==========================
# Directories
# ==========================
PROJECT_ROOT = Path(__file__).parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"

RAW_HISTORICAL_DIR = RAW_DIR / "historical"
RAW_REALTIME_DIR = RAW_DIR / "realtime"