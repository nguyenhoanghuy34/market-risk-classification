import pandas as pd
from pathlib import Path


# ==================================================
# Data path
# ==================================================

DATA_PATH = Path(
    "data/raw/historical/BTCUSDT/BTCUSDT_1m.csv"
)


# ==================================================
# Load data
# ==================================================

def load_data():

    return pd.read_csv(DATA_PATH)


# ==================================================
# Test file exists
# ==================================================

def test_file_exists():

    assert DATA_PATH.exists(), (
        f"Data file not found: {DATA_PATH}"
    )


# ==================================================
# Test read csv
# ==================================================

def test_read_csv():

    df = load_data()

    assert isinstance(df, pd.DataFrame)

    assert len(df) > 0


# ==================================================
# Test schema
# ==================================================

def test_columns():

    df = load_data()


    required_columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "number_of_trades",
    ]


    for column in required_columns:

        assert column in df.columns, (
            f"Missing column: {column}"
        )


# ==================================================
# Test missing values
# ==================================================

def test_missing_values():

    df = load_data()


    missing = df.isnull().sum().sum()


    assert missing == 0, (
        f"Found {missing} missing values"
    )


# ==================================================
# Test datatype
# ==================================================

def test_numeric_columns():

    df = load_data()


    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]


    for column in numeric_columns:

        assert pd.api.types.is_numeric_dtype(
            df[column]
        ), (
            f"{column} is not numeric"
        )


# ==================================================
# Test price validity
# ==================================================

def test_price_positive():

    df = load_data()


    price_columns = [
        "open",
        "high",
        "low",
        "close",
    ]


    for column in price_columns:

        assert (
            df[column] > 0
        ).all(), (
            f"{column} contains invalid price"
        )


# ==================================================
# Test volume
# ==================================================

def test_volume_positive():

    df = load_data()


    assert (
        df["volume"] >= 0
    ).all()


# ==================================================
# Test duplicate timestamp
# ==================================================

def test_duplicate_timestamp():

    df = load_data()


    duplicate_count = (
        df["open_time"]
        .duplicated()
        .sum()
    )


    assert duplicate_count == 0, (
        f"Found {duplicate_count} duplicated timestamps"
    )