from datetime import datetime, timedelta

from scraper.client import SGXClient


def main():

    client = SGXClient()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    announcements = client.get_company_announcement(
        "OILTEK INTERNATIONAL LIMITED",
        period_start=start_date.strftime("%Y%m%d_000000"),
        period_end=end_date.strftime("%Y%m%d_235959")
    )

    print()
    print(f"Found {len(announcements)} announcements")
    print("=" * 60)
    print()

    if not announcements:
        print("No announcements found.")
        return

    first = announcements[0]

    print("First Announcement:")
    print(f"  {first}")
    print()
    print(f"  Title: {first.title}")
    print(f"  Company: {first.company_name}")
    print(f"  Stock Code: {first.stock_code}")
    print(f"  Date: {first.submission_date}")
    print(f"  Announcement URL: {first.announcement_url}")

if __name__ == "__main__":

    main()