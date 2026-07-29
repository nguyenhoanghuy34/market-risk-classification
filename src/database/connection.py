import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def create_db_engine():

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(
        url,
        echo=False,
        future=True,
    )


def create_db_session():

    engine = create_db_engine()

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )