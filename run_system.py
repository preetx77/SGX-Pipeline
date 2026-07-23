import logging
import threading
import time

from config.watchlist import WATCHLIST
from services.market_ingestor import MarketIngestor
from utils.logger import setup_logger
from watchers.sgx_watcher import SGXWatcher


INGEST_INTERVAL = 60
WATCH_INTERVAL = 5


def ingestor_loop():

    ingestor = MarketIngestor()

    while True:

        try:
            ingestor.run_once(WATCHLIST)

        except Exception:
            logging.exception("Market ingestor failed.")

        time.sleep(INGEST_INTERVAL)


def watcher_loop():

    watcher = SGXWatcher()

    while True:

        try:
            watcher.run_once()

        except Exception:
            logging.exception("Watcher failed.")

        time.sleep(WATCH_INTERVAL)


def main():

    setup_logger()

    logging.info("Starting SGX Monitoring System...")

    threading.Thread(
        target=ingestor_loop,
        daemon=True
    ).start()

    threading.Thread(
        target=watcher_loop,
        daemon=True
    ).start()

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        logging.info("Stopping system...")


if __name__ == "__main__":
    main()