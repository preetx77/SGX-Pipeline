from datetime import datetime, timedelta
from services.announcement_service import AnnouncementService


# Watchlist of companies to sync
WATCHLIST = [
    ("OILTEK INTERNATIONAL LIMITED", "HQU"),
    ("HYPHENS PHARMA INTERNATIONAL LIMITED", "HPI"),
    ("CNMC GOLDMINE HOLDINGS LIMITED", "CGH"),
    ("TREK 2000 INTERNATIONAL LTD", "T2K"),
]


def main():

    service = AnnouncementService()
    
    # Get announcements from last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    summary = service.sync_watchlist(
        WATCHLIST,
        period_start=start_date.strftime("%Y%m%d_000000"),
        period_end=end_date.strftime("%Y%m%d_235959")
    )

    print()
    print("=" * 70)
    print("Watchlist Sync Report")
    print("=" * 70)
    print(f"Total Companies: {summary['total_companies']}")
    print(f"Total Fetched:   {summary['total_fetched']}")
    print(f"Total Inserted:  {summary['total_inserted']}")
    print(f"Total Skipped:   {summary['total_skipped']}")
    print("=" * 70)
    print()

    for company_result in summary['companies']:
        print(f"[{company_result.get('stock_code', 'N/A')}] {company_result['company']}")
        if 'error' in company_result:
            print(f"  ERROR: {company_result['error']}")
        else:
            print(f"  Fetched: {company_result['fetched']} | Inserted: {company_result['inserted']} | Skipped: {company_result['skipped']}")
    
    print()

    service.close()


if __name__ == "__main__":
    main()
