# announcement service
# coordinates the SGX client and repository

from datetime import datetime, timedelta
from scraper.client import SGXClient
from database.repository import AnnouncementRepository


class AnnouncementService:

    def __init__(self):
        self.client = SGXClient()
        self.repository = AnnouncementRepository()

    def sync_company(
        self,
        company_name,
        period_start=None,
        period_end=None
    ):
        """Sync announcements for a single company"""
        
        # If dates not provided, use defaults
        if period_start is None or period_end is None:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            period_start = start_date.strftime("%Y%m%d_%H%M%S")
            period_end = end_date.strftime("%Y%m%d_%H%M%S")

        announcements = self.client.get_company_announcement(
            company_name,
            period_start=period_start,
            period_end=period_end
        )

        inserted = 0
        skipped = 0

        for announcement in announcements:
            if self.repository.insert(announcement):
                inserted += 1
            else:
                skipped += 1

        return {
            "company": company_name,
            "period_start": period_start,
            "period_end": period_end,
            "fetched": len(announcements),
            "inserted": inserted,
            "skipped": skipped
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
        
        for company_name, stock_code in watchlist:
            try:
                result = self.sync_company(
                    company_name,
                    period_start=period_start,
                    period_end=period_end
                )
                
                # Update totals
                summary["total_fetched"] += result["fetched"]
                summary["total_inserted"] += result["inserted"]
                summary["total_skipped"] += result["skipped"]
                
                # Add company result
                summary["companies"].append({
                    "company": company_name,
                    "stock_code": stock_code,
                    "fetched": result["fetched"],
                    "inserted": result["inserted"],
                    "skipped": result["skipped"]
                })
                
            except Exception as e:
                summary["companies"].append({
                    "company": company_name,
                    "stock_code": stock_code,
                    "error": str(e)
                })
        
        return summary

    def close(self):
        self.repository.close()
