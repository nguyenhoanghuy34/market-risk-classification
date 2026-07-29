"""
PostgreSQL connection.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_database_url() -> str:
    """
    Build PostgreSQL connection URL.
    """
    return (
        "postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )


def create_db_engine():
    """
    Create SQLAlchemy engine.
    """
    return create_engine(
        get_database_url(),
        echo=False,
        future=True,
    )


def create_db_session():
    """
    Create SQLAlchemy session factory.
    """
    engine = create_db_engine()

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )