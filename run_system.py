import logging
import threading
import time
import atexit
from pathlib import Path

from config.watchlist_500 import WATCHLIST
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
    
    # Note: We do NOT close repositories here to avoid premature connection closure
    # while threads might still be using them. Let the process exit normally.
    # Each DatabaseManager connection will be closed by the OS when the process terminates.
    
    # Remove process start file on clean shutdown
    try:
        Path("state/process_started.txt").unlink()
    except:
        pass


def validate_startup(watchlist):
    """Validate that watchlist was loaded with minimum required companies.
    
    Raises:
        ValueError: If fewer than expected companies loaded or duplicates found.
    """
    MIN_COMPANIES = len(watchlist)
    codes = [c.code for c in watchlist]
    unique_codes = set(codes)
    
    logging.info(f"WATCHLIST Configured: {len(watchlist)} Loaded: {len(codes)}")
    
    if len(codes) < MIN_COMPANIES:
        raise ValueError(
            f"STARTUP VALIDATION FAILED: "
            f"Configured {MIN_COMPANIES} companies but only loaded {len(codes)}"
        )
    
    if len(codes) != len(unique_codes):
        duplicates = [c for c in unique_codes if codes.count(c) > 1]
        raise ValueError(
            f"STARTUP VALIDATION FAILED: "
            f"Duplicate company codes detected: {duplicates}"
        )
    
    logging.info(f"Watchlist validation PASSED: {len(unique_codes)} unique codes")


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
    
    # Validate watchlist on startup
    try:
        validate_startup(WATCHLIST)
    except ValueError as e:
        logging.error(str(e))
        raise
    
    # Log instrumentation startup message
    logging.info(
        "Comprehensive monitoring enabled: "
        "request counts, cache metrics, HTTP status distribution, "
        "error classification (DNS, timeout, connection drop, DB), "
        "company query coverage tracking"
    )

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
