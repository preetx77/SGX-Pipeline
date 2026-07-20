from scraper.client import SGXClient
from database.announcement_repository import AnnouncementRepository


class BackfillService:

    def __init__(self):
        self.client = SGXClient()
        self.repo = AnnouncementRepository()

    def backfill_company(
        self,
        company_name,
        period_start,
        period_end,
    ):

        inserted = 0
        skipped = 0

        print(f"\nBackfilling {company_name}\n")

        for announcement in self.client.iter_company_announcements(
            company_name=company_name,
            period_start=period_start,
            period_end=period_end,
        ):

            if self.repo.exists(announcement.announcement_id):
                skipped += 1
                continue

            self.repo.insert(announcement)
            inserted += 1

            print(
                f"[{inserted:03d}] "
                f"{announcement.submission_date} "
                f"{announcement.title}"
            )

        print("\n==========================")
        print(f"Inserted : {inserted}")
        print(f"Skipped  : {skipped}")
        print("==========================")