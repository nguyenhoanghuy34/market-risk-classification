"""
Generate a training summary from MLflow SQLite database.

Usage:
    python -m src.utils.mlflow_summary
"""

from pathlib import Path

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MLFLOW_DB = PROJECT_ROOT / "artifacts" / "mlflow.db"
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_FILE = REPORT_DIR / "mlflow_summary.txt"


def main() -> None:
    print(f"MLflow DB : {MLFLOW_DB}")
    print(f"Report    : {REPORT_FILE}")

    if not MLFLOW_DB.exists():
        raise FileNotFoundError(f"Cannot find: {MLFLOW_DB}")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()