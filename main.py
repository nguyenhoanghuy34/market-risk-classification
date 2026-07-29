from src.etl.pipeline import ETLPipeline
from src.database.test_db import test_database_connection

def main():

    #pipeline = ETLPipeline()
    #pipeline.run()
    test_database_connection()

if __name__ == "__main__":
    main()