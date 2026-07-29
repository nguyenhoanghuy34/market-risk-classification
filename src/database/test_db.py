"""
Test PostgreSQL connection.
"""

from sqlalchemy import text

from src.database.connection import create_db_engine


def test_database_connection():
    """
    Test database connection.
    """
    engine = create_db_engine()

    try:
        with engine.connect() as connection:
            version = connection.execute(
                text("SELECT version();")
            ).scalar_one()

        print("=" * 60)
        print("Database connected successfully.")
        print(version)
        print("=" * 60)

    except Exception as error:
        print("=" * 60)
        print("Database connection failed.")
        print(error)
        print("=" * 60)