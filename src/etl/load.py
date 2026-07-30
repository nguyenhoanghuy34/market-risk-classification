from pathlib import Path
import pandas as pd


def load(df: pd.DataFrame, path: str | Path):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        path,
        index=False,
    )