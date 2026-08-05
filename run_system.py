import logging
import threading
import time
import atexit
from pathlib import Path

from config.watchlist import WATCHLIST
from services.market_ingestor import MarketIngestor
from utils.logger import setup_logger
from watchers.sgx_watcher import SGXWatcher


INGEST_INTERVAL = 60
WATCH_INTERVAL = 5

ingestor = None
watcher = None


def cleanup():
    """Clean up resources on shutdown"""
    global ingestor, watcher
    
    logging.info("Cleaning up resources...")
    
    if ingestor:
        ingestor.close()
    
    if watcher:
        try:
            watcher.repo.close()
        except Exception as e:
            logging.warning(f"Failed to close watcher repository: {e}")
    
    # Remove process start file on clean shutdown
    try:
        Path("state/process_started.txt").unlink()
    except:
        pass


def ingestor_loop():

    global ingestor
    ingestor = MarketIngestor()

    while True:

        try:
            ingestor.run_once(WATCHLIST)

        except Exception:
            logging.exception("Market ingestor failed.")

        time.sleep(INGEST_INTERVAL)


def watcher_loop():

    global watcher
    watcher = SGXWatcher()

    while True:

        try:
            watcher.run_once()

        except Exception:
            logging.exception("Watcher failed.")

        time.sleep(WATCH_INTERVAL)


def main():

    setup_logger()
    
    # Write process start time immediately
    from datetime import datetime
    process_start_file = Path("state/process_started.txt")
    process_start_file.parent.mkdir(parents=True, exist_ok=True)
    process_start_file.write_text(datetime.now().isoformat())
    
    # Register cleanup function
    atexit.register(cleanup)

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
        cleanup()


if __name__ == "__main__":
    main()