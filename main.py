from services.announcement_service import AnnouncementService


WATCHLIST = [

    ("OILTEK INTERNATIONAL LIMITED", "HQU"),

    ("HYPHENS PHARMA INTERNATIONAL LIMITED", "HPI"),

    ("CNMC GOLDMINE HOLDINGS LIMITED", "CGH"),

    ("TREK 2000 INTERNATIONAL LTD", "T2K")

]


def main():

    service = AnnouncementService()

    total_announcements = 0

    total_documents = 0

    total_downloaded = 0

    print()

    print("=" * 90)

    print("SGX PIPELINE")

    print("=" * 90)

    print()

    for company, code in WATCHLIST:

        result = service.sync_company(

            company,

            code

        )

        total_announcements += result["announcements_fetched"]

        total_documents += result["attachments_discovered"]

        total_downloaded += result["attachments_downloaded"]

        print(f"[{code}] {company}")

        print(

            f"Announcements : "

            f"{result['announcements_fetched']}"

        )

        print(

            f"Documents     : "

            f"{result['attachments_discovered']}"

        )

        print(

            f"Downloaded    : "

            f"{result['attachments_downloaded']}"

        )

        print()

    print("=" * 90)

    print("SUMMARY")

    print("=" * 90)

    print(f"Companies      : {len(WATCHLIST)}")

    print(f"Announcements  : {total_announcements}")

    print(f"Documents      : {total_documents}")

    print(f"New Downloads  : {total_downloaded}")

    print("=" * 90)

    service.close()


if __name__ == "__main__":

    main()