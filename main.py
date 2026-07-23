from src.etl.pipeline import ETLPipeline

def main():

    pipeline = ETLPipeline()
    pipeline.run()

if __name__ == "__main__":
    main()