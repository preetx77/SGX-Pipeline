import time

from config.watchlist import WATCHLIST
from services.market_ingestor import MarketIngestor
from utils.logger import setup_logger


def main():

    setup_logger()

    ingestor = MarketIngestor()

    try:

        while True:

            ingestor.run_once(WATCHLIST)

            time.sleep(60)

    except KeyboardInterrupt:

        print("\nStopping...")

    finally:

        ingestor.close()


if __name__ == "__main__":
    main()