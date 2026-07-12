from database.repository import AnnouncementRepository


def main():

    repo = AnnouncementRepository()

    print()

    print("=" * 60)

    print("Database Statistics")

    print("=" * 60)

    print(f"Total announcements : {repo.count()}")

    latest = repo.get_latest()

    print()

    print("Latest announcement")

    print("-------------------")

    print(latest["title"])

    print(latest["company_name"])

    print(latest["submission_date"])

    repo.close()


if __name__ == "__main__":

    main()