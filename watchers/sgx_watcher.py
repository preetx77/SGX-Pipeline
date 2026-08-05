from database.announcement_repository import AnnouncementRepository
from database.document_repository import DocumentRepository
from notifications.telegram_notifier import TelegramNotifier
from services.insider_pipeline import InsiderPipeline
from events.event_engine import EventEngine
from state.state_manager import StateManager
from core.classifier import classify

import logging

class SGXWatcher:

    def __init__(self):

        self.repo = AnnouncementRepository()
        self.doc_repo = DocumentRepository()
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

            # Classify announcement
            classification = classify(announcement)
            logging.info(
                f"Classification: {classification.event_type.value} | "
                f"Priority: {classification.priority.label} {classification.priority.stars}"
            )

            # Process insider dealings with documents
            documents = self.doc_repo.get_documents_by_announcement(
                announcement.announcement_id
            )
            
            if documents:
                try:
                    self.insider_pipeline.process(announcement, documents)
                except Exception as e:
                    logging.error(
                        f"Failed to process insider pipeline for {announcement.announcement_id}: {e}"
                    )

            # Process corporate events
            events = self.event_engine.process(announcement)

            for event in events:
                logging.info(
                    f"Corporate event detected: {event.event_type} - {event.title}"
                )

            # Notify based on classification priority
            if classification.priority.notify:
                try:
                    # Use notify_announcement for generic announcements
                    self.notifier.notify_announcement(
                        announcement.company_name,
                        announcement
                    )
                    logging.info(
                        f"Announcement notification sent for {announcement.announcement_id}"
                    )
                except Exception as e:
                    logging.error(
                        f"Failed to send announcement notification for {announcement.announcement_id}: {e}"
                    )

            newest_id = announcement.announcement_id

        if newest_id is not None:
            self.state.save_last_id(newest_id)
            logging.info("Checkpoint updated.")

