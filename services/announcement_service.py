# announcement service
# coordinates the SGX client and repository

from datetime import datetime, timedelta
from scraper.client import SGXClient
from database.announcement_repository import AnnouncementRepository
from services.attachment_service import AttachmentService

class AnnouncementService:

    def __init__(self):
        self.client = SGXClient()
        self.repository = AnnouncementRepository()
        self.attachment_service = AttachmentService()

    def sync_company(self, company_name, stock_code):
        """Sync announcements for a single company"""
        
        latest_timestamp = self.repository.get_latest_timestamp(company.code)
        
        end = datetime.now()
        
        if latest_timestamp:
            # latest_timestamp is in milliseconds, convert to seconds
            from datetime import datetime as dt
            latest_date = dt.fromtimestamp(latest_timestamp / 1000)
            start = latest_date - timedelta(days=1)
        else:
            start = end - timedelta(days=90)
        
        period_start = start.strftime("%Y%m%d_000000")
        period_end = end.strftime("%Y%m%d_235959")
        
        announcements = self.client.get_company_announcement(
            company.name,
            period_start=period_start,
            period_end=period_end
        )

        print(f"\n===== {company_name} =====")
        print(f"Period Start : {period_start}")
        print(f"Period End   : {period_end}")
        print(f"Announcements Returned : {len(announcements)}\n")

        for announcement in announcements:
            print(
                f"{announcement.submission_date} | "
                f"{announcement.announcement_id} | "
                f"{announcement.title}"
            )

        print("=" * 60)
        
        inserted = 0
        skipped = 0
        attachment_discovered = 0
        attachment_inserted = 0
        attachment_downloaded = 0
        attachment_skipped = 0
        
        for announcement in announcements:
            is_new = self.repository.insert(announcement)
            
            if is_new:
                inserted += 1
            else:
                skipped += 1
            
            attachment_result = self.attachment_service.process_announcement(announcement)
            
            attachment_discovered += len(
                attachment_result["attachments"]
            )

            attachment_inserted += len(
                attachment_result["new"]
            )

            attachment_downloaded += len(
                attachment_result["downloaded"]
            )

            attachment_skipped += len(
                attachment_result["existing"]
            )
        
        return {
            "company": company.name,
            "stock_code": company.code,
            "period_start": period_start,
            "period_end": period_end,
            "announcements_fetched": len(announcements),
            "announcements_inserted": inserted,
            "announcements_skipped": skipped,
            "attachments_discovered": attachment_discovered,
            "attachments_inserted": attachment_inserted,
            "attachments_downloaded": attachment_downloaded,
            "attachments_skipped": attachment_skipped
        }

    def sync_watchlist(
        self,
        watchlist,
        period_start=None,
        period_end=None
    ):
        """Sync announcements for multiple companies in watchlist"""
        
        # If dates not provided, use defaults
        if period_start is None or period_end is None:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            period_start = start_date.strftime("%Y%m%d_%H%M%S")
            period_end = end_date.strftime("%Y%m%d_%H%M%S")
        
        summary = {
            "total_companies": len(watchlist),
            "total_fetched": 0,
            "total_inserted": 0,
            "total_skipped": 0,
            "companies": []
        }
        
        for company in watchlist:
            try:
                result = self.sync_company(
                    company.name,
                    company.code
                )
                
                # Update totals
                summary["total_fetched"] += result["announcements_fetched"]
                summary["total_inserted"] += result["announcements_inserted"]
                summary["total_skipped"] += result["announcements_skipped"]
                
                # Add company result
                summary["companies"].append({
                    "company": company.name,
                    "stock_code": company.code,
                    "fetched": result["announcements_fetched"],
                    "inserted": result["announcements_inserted"],
                    "skipped": result["announcements_skipped"]
                })
                
            except Exception as e:
                summary["companies"].append({
                    "company": company.name,
                    "stock_code": company.code,
                    "error": str(e)
                })
        
        return summary

    def close(self):
        self.repository.close()
        self.attachment_service.close()
