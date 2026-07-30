from pathlib import Path

# ==================================================
# Project
# ==================================================
PROJECT_ROOT = Path(__file__).resolve().parent

# ==================================================
# Binance
# ==================================================
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

# ==================================================
# Directories
# ==================================================
DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"

RAW_HISTORICAL_DIR = RAW_DIR / "historical"
RAW_REALTIME_DIR = RAW_DIR / "realtime"

# ==================================================
# Artifacts
# ==================================================
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

MLRUNS_DIR = ARTIFACTS_DIR / "mlruns"

# ==================================================
# MLflow
# ==================================================
MLFLOW_DB = PROJECT_ROOT / "artifacts" / "mlflow.db"

MLFLOW_TRACKING_URI = f"sqlite:///{MLFLOW_DB}"

MLFLOW_ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "mlruns"

MLFLOW_EXPERIMENT_NAME = "Market Risk Classification"