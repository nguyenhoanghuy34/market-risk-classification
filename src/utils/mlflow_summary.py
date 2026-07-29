"""
Generate a readable training summary from MLflow SQLite database.

Usage:
    python -m src.utils.mlflow_summary
"""

# ==========================================================
# Imports
# ==========================================================

import sqlite3
from pathlib import Path


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_DIR = PROJECT_ROOT / "artifacts"

MLFLOW_DB = ARTIFACT_DIR / "mlflow.db"

REPORT_DIR = PROJECT_ROOT / "reports"

REPORT_FILE = REPORT_DIR / "mlflow_summary.txt"

# ==========================================================
# Database
# ==========================================================

def connect_db() -> sqlite3.Connection:
    """
    Connect to MLflow SQLite database.
    """

    if not MLFLOW_DB.exists():
        raise FileNotFoundError(
            f"MLflow database not found:\n{MLFLOW_DB}"
        )

    return sqlite3.connect(MLFLOW_DB)


def execute_query(
    conn: sqlite3.Connection,
    query: str,
):
    """
    Execute SQL query and return all rows.
    """

    cursor = conn.cursor()

    cursor.execute(query)

    return cursor.fetchall()

# ==========================================================
# Query
# ==========================================================

def get_experiments(conn: sqlite3.Connection):
    """
    Return all active experiments.
    """

    query = """
        SELECT
            experiment_id,
            name
        FROM experiments
        WHERE lifecycle_stage = 'active'
        ORDER BY experiment_id;
    """

    return execute_query(conn, query)


def get_runs(conn: sqlite3.Connection):
    """
    Return all finished runs.
    """

    query = """
        SELECT
            run_uuid,
            experiment_id,
            status,
            start_time,
            end_time
        FROM runs
        WHERE lifecycle_stage = 'active'
        ORDER BY start_time DESC;
    """

    return execute_query(conn, query)


def get_metrics(conn: sqlite3.Connection):
    """
    Return all latest metrics.
    """

    query = """
        SELECT
            run_uuid,
            key,
            value
        FROM latest_metrics;
    """

    return execute_query(conn, query)


def get_params(conn: sqlite3.Connection):
    """
    Return all parameters.
    """

    query = """
        SELECT
            run_uuid,
            key,
            value
        FROM params;
    """

    return execute_query(conn, query)


# ==========================================================
# Builder
# ==========================================================

from collections import defaultdict


def build_run_summary(
    runs,
    metrics,
    params,
):
    """
    Merge runs, metrics and params into a single structure.

    Returns
    -------
    list[dict]
    """

    # -----------------------------
    # Metrics
    # -----------------------------

    metric_map = defaultdict(dict)

    for run_uuid, key, value in metrics:
        metric_map[run_uuid][key] = value

    # -----------------------------
    # Params
    # -----------------------------

    param_map = defaultdict(dict)

    for run_uuid, key, value in params:
        param_map[run_uuid][key] = value

    # -----------------------------
    # Merge
    # -----------------------------

    summary = []

    for (
        run_uuid,
        experiment_id,
        status,
        start_time,
        end_time,
    ) in runs:

        run = {
            "run_id": run_uuid,
            "experiment_id": experiment_id,
            "status": status,
            "start_time": start_time,
            "end_time": end_time,
            "metrics": metric_map.get(run_uuid, {}),
            "params": param_map.get(run_uuid, {}),
        }

        summary.append(run)

    return summary


# ==========================================================
# Formatter
# ==========================================================

from datetime import datetime


def format_timestamp(timestamp_ms):
    """
    Convert MLflow timestamp (milliseconds) to readable datetime.
    """

    if timestamp_ms is None:
        return "-"

    return datetime.fromtimestamp(
        timestamp_ms / 1000
    ).strftime("%Y-%m-%d %H:%M:%S")


def format_duration(start_ms, end_ms):
    """
    Convert milliseconds to seconds.
    """

    if start_ms is None or end_ms is None:
        return "-"

    seconds = (end_ms - start_ms) / 1000

    return f"{seconds:.2f} s"


def format_metric(metrics, key):
    """
    Return metric with 4 decimal places.
    """

    value = metrics.get(key)

    if value is None:
        return "-"

    return f"{float(value):.4f}"


def get_model_name(params):
    """
    Return model name from MLflow params.

    Fallback if not found.
    """

    for key in (
        "model_name",
        "model",
        "classifier",
        "algorithm",
    ):
        if key in params:
            return params[key]

    return "Unknown"


# ==========================================================
# Report
# ==========================================================

def build_report(summary):
    """
    Build report text.
    """

    lines = []

    separator = "=" * 120
    divider = "-" * 120

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    lines.append(separator)
    lines.append("MLFLOW TRAINING HISTORY")
    lines.append(separator)
    lines.append("")

    header = (
        f"{'No':<4}"
        f"{'Model':<24}"
        f"{'Accuracy':<11}"
        f"{'Precision':<11}"
        f"{'Recall':<11}"
        f"{'F1':<11}"
        f"{'Time':<10}"
        f"{'Status':<12}"
        f"{'Created'}"
    )

    lines.append(header)
    lines.append(divider)

    # ------------------------------------------------------
    # Body
    # ------------------------------------------------------

    best_accuracy = -1.0
    best_model = "-"
    latest_run = "-"

    for index, run in enumerate(summary, start=1):

        lines.append(
            build_table_row(index, run)
        )

        model_name = get_model_name(run["params"])

        accuracy = run["metrics"].get("accuracy")

        if accuracy is not None:

            accuracy = float(accuracy)

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model_name

        latest_run = model_name

    # ------------------------------------------------------
    # Footer
    # ------------------------------------------------------

    lines.append(divider)
    lines.append("")

    lines.append(f"Total Runs      : {len(summary)}")

    if best_accuracy >= 0:
        lines.append(
            f"Best Accuracy   : {best_model} ({best_accuracy:.4f})"
        )
    else:
        lines.append(
            "Best Accuracy   : -"
        )

    lines.append(
        f"Latest Run      : {latest_run}"
    )

    return "\n".join(lines)


def build_table_row(index, run):
    metrics = run["metrics"]
    params = run["params"]

    return (
        f"{index:<4}"
        f"{get_model_name(params):<24}"
        f"{format_metric(metrics, 'accuracy'):<11}"
        f"{format_metric(metrics, 'precision'):<11}"
        f"{format_metric(metrics, 'recall'):<11}"
        f"{format_metric(metrics, 'f1_score'):<11}"
        f"{format_duration(run['start_time'], run['end_time']):<10}"
        f"{run['status']:<12}"
        f"{format_timestamp(run['start_time'])}"
    )

# ==========================================================
# Writer
# ==========================================================

def save_report(report: str) -> bool:
    """
    Save report only if its content has changed.

    Returns
    -------
    bool
        True if report was updated.
        False if nothing changed.
    """

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if REPORT_FILE.exists():

        current = REPORT_FILE.read_text(
            encoding="utf-8"
        )

        if current == report:
            return False

    REPORT_FILE.write_text(
        report,
        encoding="utf-8",
    )

    return True


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("MLflow Summary")
    print("=" * 60)

    conn = connect_db()

    try:

        runs = get_runs(conn)

        metrics = get_metrics(conn)

        params = get_params(conn)

    finally:

        conn.close()

    summary = build_run_summary(
        runs,
        metrics,
        params,
    )

    report = build_report(summary)

    updated = save_report(report)

    print()

    print(f"Runs Found : {len(summary)}")

    if updated:
        print("Report updated.")
    else:
        print("Report already up-to-date.")

    print(f"Output : {REPORT_FILE}")


if __name__ == "__main__":
    main()

