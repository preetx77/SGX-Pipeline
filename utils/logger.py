import sys
from pathlib import Path

# Add parent directory to path so imports work from any location
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging


def setup_logger():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )