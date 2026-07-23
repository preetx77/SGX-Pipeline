from database.announcement_repository import AnnouncementRepository
from notifications.telegram_notifier import TelegramNotifier
from pipeline.sgx_pipeline import SGXPipeline
from state.state_manager import StateManager

import logging

class SGXWatcher:

    def __init__(self):

        self.repo = AnnouncementRepository()
        self.pipeline = SGXPipeline()
        self.state = StateManager()
        self.notifier = TelegramNotifier()

    def run_once(self):

        logging.info("Checking for new announcements...")

        last_processed = self.state.get_last_id()

        logging.info(
            "Last checkpoint: %s",
            last_processed
        )

        announcements = self.repo.get_after(last_processed)

        if not announcements:

            logging.info("No new announcements.")

            return

        logging.info(
            "Found %d new announcement(s)",
            len(announcements)
        )

        newest_id = last_processed

        for announcement in announcements:

            logging.info(
                "Processing [%s] %s",
                announcement.stock_code,
                announcement.company_name
            )

            signal = self.pipeline.process(announcement)

            if signal is not None:
                self.notifier.notify(signal)

            newest_id = announcement.announcement_id

        if newest_id is not None:
            self.state.save_last_id(newest_id)
            logging.info("Checkpoint updated.")

