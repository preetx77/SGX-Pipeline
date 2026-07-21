from database.announcement_repository import AnnouncementRepository
from notifications.telegram_notifier import TelegramNotifier
from pipeline.sgx_pipeline import SGXPipeline
from state.state_manager import StateManager
from config.watchlist import WATCHLIST


class SGXWatcher:

    def __init__(self):

        self.repo = AnnouncementRepository()
        self.pipeline = SGXPipeline()
        self.state = StateManager()
        self.notifier = TelegramNotifier()

    def run_once(self):

        print("\nChecking for new announcements...\n")

        announcements = self.repo.latest(50)

        print("\n===== Latest Announcements =====\n")

        for announcement in announcements:

            print(
                announcement.stock_code,
                "|",
                announcement.company_name,
                "|",
                announcement.title
            )

        print("\n===============================\n")

        if not announcements:

            print("No announcements found.")

            return

        last_processed = self.state.get_last_id()

        print(f"Last Processed : {last_processed}")

        new_announcements = []

        for announcement in announcements:
            if announcement.announcement_id == last_processed:
                break

            new_announcements.append(announcement)

        if not new_announcements:
            print("\nNo new announcements.\n")

            return

        print(f"\nFound {len(new_announcements)} new announcement(s).\n")

        # Process oldest → newest
        new_announcements.reverse()

        for announcement in new_announcements:

            if announcement.stock_code not in WATCHLIST:

                print(
                    f"Skipping : {announcement.stock_code}"
                )

                continue

            print(
                f"Processing : [{announcement.stock_code}] "
                f"{announcement.company_name}"
            )

            signal = self.pipeline.process(
                announcement
            )
            if signal is not None:
                self.notifier.notify(signal)

            self.state.save_last_id(
                announcement.announcement_id
            )

        print("\nCheckpoint updated.")