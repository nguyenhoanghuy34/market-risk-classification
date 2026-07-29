"""
Inspect MLflow SQLite database schema.

Usage:
    python -m src.utils.check_mlflow_db
"""

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MLFLOW_DB = PROJECT_ROOT / "artifacts" / "mlflow.db"


def main() -> None:

    conn = sqlite3.connect(MLFLOW_DB)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """)

    tables = [row[0] for row in cursor.fetchall()]

    print("=" * 80)
    print("MLFLOW DATABASE SCHEMA")
    print("=" * 80)

    for table in tables:

        print()
        print("=" * 80)
        print(f"TABLE: {table}")
        print("=" * 80)

        cursor.execute(f"PRAGMA table_info({table});")

        columns = cursor.fetchall()

        for column in columns:
            cid, name, dtype, notnull, default, pk = column

            print(
                f"{cid:>2} | "
                f"{name:<30} | "
                f"{dtype:<15} | "
                f"PK={pk}"
            )

    conn.close()


if __name__ == "__main__":
    main()