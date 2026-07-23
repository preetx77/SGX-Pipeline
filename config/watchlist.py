WATCHLIST = [
    ("OILTEK INTERNATIONAL LIMITED", "HQU"),
]

WATCHLIST_CODES = {
    stock_code
    for _, stock_code in WATCHLIST
}


# Why tuples?  :  Because AnnouncementService.sync_company() needs: