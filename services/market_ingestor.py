from services.announcement_service import AnnouncementService


class MarketIngestor:
    """
    Continuously synchronizes the configured watchlist
    into the local SQLite database.
    """

    def __init__(self):
        self.service = AnnouncementService()

    def run_once(self, watchlist):

        print("\n========== MARKET INGESTION ==========\n")

        summary = self.service.sync_watchlist(
            watchlist=watchlist
        )

        print(f"Companies Scanned : {summary['total_companies']}")
        print(f"Announcements Fetched : {summary['total_fetched']}")
        print(f"Inserted : {summary['total_inserted']}")
        print(f"Skipped : {summary['total_skipped']}")

        print("\nPer Company\n")

        for company in summary["companies"]:

            if "error" in company:

                print(
                    f"[ERROR] "
                    f"{company['company']} : "
                    f"{company['error']}"
                )

                continue

            print(
                f"[{company['stock_code']}] "
                f"{company['company']} | "
                f"Fetched={company['fetched']} | "
                f"Inserted={company['inserted']} | "
                f"Skipped={company['skipped']}"
            )

        print("\n======================================\n")

        return summary

    def close(self):
        self.service.close()