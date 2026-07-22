from src.data_collection.historical_downloader import HistoricalDownloader


def main():

    downloader = HistoricalDownloader()

    downloader.download(
        symbol="BTCUSDT",
        interval="1m",
        start_date="1 Jan, 2025",
        end_date="15 Jan, 2025",
    )


if __name__ == "__main__":
    main()