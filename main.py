from configs import (
    WATCHLIST,
    BACKFILL_START,
    BACKFILL_END
)

from scraper.client import SGXClient


def main():

    client = SGXClient()

    result = client.get_company_announcement_page(

        company_name=WATCHLIST[0],

        period_start=BACKFILL_START,

        period_end=BACKFILL_END,

        page_start=100,
        page_size=100

    )

    meta = result["meta"]

    announcements = result["announcements"]

    print()

    print("=" * 70)

    print("Historical Backfill Test")

    print("=" * 70)

    print("Company     :", WATCHLIST[0])

    print("Total Items :", meta["totalItems"])

    print("Total Pages :", meta["totalPages"])

    print("Fetched     :", len(announcements))

    print()

    print(f"Fetched : {len(announcements)}")
    
    if announcements:
        print("\nFirst")
        print("-----")
        print(announcements[0])
        
        print("\nLast")
        print("----")
        print(announcements[-1])
    else:
        print("\nNo announcements returned.")
    
    print("=" * 70)

    print()

    print(meta)


if __name__ == "__main__":
    main()