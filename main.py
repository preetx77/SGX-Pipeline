from datetime import datetime, timedelta
from services.announcement_service import AnnouncementService


def main():

    service = AnnouncementService()
    
    # Get announcements from last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    result = service.sync_company(
        "OILTEK INTERNATIONAL LIMITED",
        period_start=start_date.strftime("%Y%m%d_000000"),
        period_end=end_date.strftime("%Y%m%d_235959")
    )

    print()

    print("=" * 60)
    print("Sync Report")
    print("=" * 60)

    for key, value in result.items():

        print(f"{key:15}: {value}")

    service.close()


if __name__ == "__main__":
    main()