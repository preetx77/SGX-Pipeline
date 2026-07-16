"""
Global Configuration
"""

from datetime import datetime


# --------------------------------------------------
# Watchlist
# --------------------------------------------------

WATCHLIST = [

    "OILTEK INTERNATIONAL LIMITED",
    "HYPHENS PHARMA INTERNATIONAL LIMITED",
    "CNMC GOLDMINE HOLDINGS LIMITED",
    "TREK 2000 INTERNATIONAL LTD"
]


# --------------------------------------------------
# Historical Backfill
# --------------------------------------------------

BACKFILL_START = "20210101_000000"

BACKFILL_END = datetime.now().strftime(
    "%Y%m%d_235959"
)


# --------------------------------------------------
# API
# --------------------------------------------------

PAGE_SIZE = 100