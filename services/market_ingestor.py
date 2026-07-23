import logging

from services.announcement_service import AnnouncementService


class MarketIngestor:

    def __init__(self):
        self.service = AnnouncementService()

    def run_once(self, watchlist):

        logging.info("Starting market synchronization...")

        summary = self.service.sync_watchlist(watchlist)

        logging.info(
            "Companies=%s | Fetched=%s | Inserted=%s | Skipped=%s",
            summary["total_companies"],
            summary["total_fetched"],
            summary["total_inserted"],
            summary["total_skipped"],
        )

        return summary

    def close(self):
        self.service.close()