import sys
import logging
from pathlib import Path

# Add parent directory to path so imports work from any location
sys.path.insert(0, str(Path(__file__).parent.parent))


def setup_logger():
    """
    Setup comprehensive logging with both console and file output.
    Essential for 24/7 unattended operation.
    """
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "sgx_pipeline.log"

    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console handler (INFO level and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    # File handler (DEBUG level and above)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logging.info(f"Logging initialized. Log file: {log_file}")