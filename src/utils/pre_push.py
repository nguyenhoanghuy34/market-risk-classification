"""
Generate MLflow summary before pushing to GitHub.
"""

import subprocess


def main():

    print("=" * 60)
    print("Generating MLflow summary...")
    print("=" * 60)

    subprocess.run(
        [
            "python",
            "-m",
            "src.utils.mlflow_summary",
        ],
        check=True,
    )

    print("=" * 60)
    print("MLflow summary updated.")
    print("=" * 60)


if __name__ == "__main__":

    main()