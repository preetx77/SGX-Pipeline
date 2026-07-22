import time

from config.watchlist import WATCHLIST
from services.market_ingestor import MarketIngestor


def main():

    ingestor = MarketIngestor()

    print("SGX Market Ingestor Started")

    try:

        while True:

            ingestor.run_once(WATCHLIST)


            print("\nSleeping for 60 seconds...\n")

            time.sleep(60)

    except KeyboardInterrupt:

        print("\nStopping Market Ingestor...")

    finally:

        ingestor.close()


if __name__ == "__main__":

    main()