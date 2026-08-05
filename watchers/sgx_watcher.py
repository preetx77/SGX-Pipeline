from database.announcement_repository import AnnouncementRepository
from notifications.telegram_notifier import TelegramNotifier
from services.insider_pipeline import InsiderPipeline
from events.event_engine import EventEngine
from state.state_manager import StateManager

import logging

class SGXWatcher:

    def __init__(self):

        self.repo = AnnouncementRepository()
        self.insider_pipeline = InsiderPipeline()
        self.event_engine = EventEngine()
        self.state = StateManager()
        self.notifier = TelegramNotifier()

    def run_once(self):

        logging.info("Checking for new announcements...")

        last_processed = self.state.get_last_id()

        logging.info(
            "Last checkpoint: %s",
            last_processed or "None (first run)"
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

            # Process insider dealings
            signal = self.insider_pipeline.process(announcement)

            if signal is not None:
                self.notifier.notify(signal)

            # Process corporate events
            events = self.event_engine.process(announcement)

            for event in events:
                logging.info(
                    f"Corporate event detected: {event.event_type} - {event.title}"
                )
                # Events are logged; extend this to notify/persist as needed
                # self.notifier.notify(event)  # Example: if notifier supports events

            newest_id = announcement.announcement_id

        if newest_id is not None:
            self.state.save_last_id(newest_id)
            logging.info("Checkpoint updated.")

