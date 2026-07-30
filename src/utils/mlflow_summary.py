"""
Generate a readable training summary from MLflow SQLite database.

Usage:
    python -m src.utils.mlflow_summary
"""

# ==========================================================
# Imports
# ==========================================================

import sqlite3

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from matplotlib import lines

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_DIR = PROJECT_ROOT / "artifacts"


# ==========================================================
# Database Helper
# ==========================================================

def execute_query(
    conn: sqlite3.Connection,
    query: str,
):
    """
    Execute SQL query and return all rows.
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()

    return rows


# ==========================================================
# Query
# ==========================================================

def get_experiments(
    conn: sqlite3.Connection,
):
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

    rows = execute_query(conn, query)

    return {
        experiment_id: name
        for experiment_id, name in rows
    }


def get_runs(
    conn: sqlite3.Connection,
):
    """
    Return all active runs.
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


def get_metrics(
    conn: sqlite3.Connection,
):
    """
    Return latest metrics of every run.
    """

    query = """
        SELECT
            run_uuid,
            key,
            value
        FROM latest_metrics;
    """

    return execute_query(conn, query)


def get_params(
    conn: sqlite3.Connection,
):
    """
    Return all parameters of every run.
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
# Processing
# ==========================================================

def build_run_summary(
    experiments,
    runs,
    metrics,
    params,
):
    """
    Combine MLflow tables into readable structure.
    """

    metric_map = {}

    for run_uuid, key, value in metrics:
        if run_uuid not in metric_map:
            metric_map[run_uuid] = {}

        metric_map[run_uuid][key] = value


    param_map = {}

    for run_uuid, key, value in params:
        if run_uuid not in param_map:
            param_map[run_uuid] = {}

        param_map[run_uuid][key] = value


    summary = []

    for (
        run_uuid,
        experiment_id,
        status,
        start_time,
        end_time,
    ) in runs:

        summary.append(
            {
                "run_id": run_uuid,
                "experiment": experiments.get(
                    experiment_id,
                    "unknown",
                ),
                "status": status,
                "start_time": start_time,
                "end_time": end_time,
                "params": param_map.get(
                    run_uuid,
                    {},
                ),
                "metrics": metric_map.get(
                    run_uuid,
                    {},
                ),
            }
        )

    return summary



# ==========================================================
# Formatting Report
# ==========================================================

def format_run_report(
    summary,
):
    """
    Convert MLflow runs into leaderboard table.
    """

    lines = []

    experiment_name = (
        summary[0]["experiment"]
        if summary
        else "Unknown"
    )

    lines.append("=" * 110)
    lines.append("MLFLOW TRAINING SUMMARY")
    lines.append(f"Experiment : {experiment_name}")
    lines.append("=" * 110)
    lines.append("")

    header = (
        f"{'No':<4}"
        f"{'Model':<25}"
        f"{'Accuracy':<10}"
        f"{'Precision':<11}"
        f"{'Recall':<10}"
        f"{'F1':<10}"
        f"{'ROC-AUC':<10}"
        f"{'Status':<12}"
        f"{'Created'}"
    )

    lines.append("=" * 110)
    lines.append(header)
    lines.append("-" * 110)


    for index, run in enumerate(summary, start=1):

        params = run["params"]
        metrics = run["metrics"]


        model = params.get(
            "model",
            "Unknown"
        )


        accuracy = metrics.get(
            "accuracy",
            0
        )

        precision = metrics.get(
            "precision",
            0
        )

        recall = metrics.get(
            "recall",
            0
        )

        f1 = metrics.get(
            "f1_score",
            0
        )

        roc_auc = metrics.get(
            "roc_auc",
            0,
        )


        training_time = metrics.get(
            "training_time",
            "-"
        )


        created = datetime.fromtimestamp(
            run["start_time"] / 1000
        ).strftime("%Y-%m-%d %H:%M")


        row = (
            f"{index:<4}"
            f"{model:<25}"
            f"{accuracy:<10.4f}"
            f"{precision:<11.4f}"
            f"{recall:<10.4f}"
            f"{f1:<10.4f}"
            f"{roc_auc:<10.4f}"
            f"{run['status']:<12}"
            f"{created}"
        )

        lines.append(row)


    lines.append("=" * 110)

    best_run = max(
        summary,
        key=lambda x: x["metrics"].get("accuracy", 0),
    )

    lines.append("")
    lines.append("=" * 110)
    lines.append(f"Total Runs    : {len(summary)}")
    lines.append(
        f"Best Accuracy : {best_run['metrics'].get('accuracy', 0):.4f}"
    )
    lines.append(
        f"Best Model    : {best_run['params'].get('model', 'Unknown')}"
    )
        
    lines.append("=" * 110)

    return "\n".join(lines)


# ==========================================================
# Save Report
# ==========================================================

def save_report(
    report: str,
    output_path: Path,
):
    """
    Save generated report to text file.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(report)


# ==========================================================
# Main
# ==========================================================

def main():

    db_path = ARTIFACT_DIR / "mlflow.db"

    output_path = (
        ARTIFACT_DIR
        / "training_summary.txt"
    )


    conn = sqlite3.connect(
        db_path
    )


    experiments = get_experiments(
        conn
    )

    runs = get_runs(
        conn
    )

    metrics = get_metrics(
        conn
    )

    params = get_params(
        conn
    )


    summary = build_run_summary(
        experiments,
        runs,
        metrics,
        params,
    )


    report = format_run_report(
        summary
    )


    save_report(
        report,
        output_path,
    )

    conn.close()

    print("=" * 60)
    print("MLflow training summary generated")
    print(f"Saved at: {output_path}")
    print("=" * 60)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()

