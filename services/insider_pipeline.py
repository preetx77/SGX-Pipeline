from extractors.insider.director_dealings_extractor import ( DirectorDealingsExtractor)

from services.signals.insider_signal_generator import (InsiderSignalGenerator)

from notifications.telegram_notifier import (TelegramNotifier)
from database.insider_signal_repository import InsiderSignalRepository
import logging

class InsiderPipeline:

    def __init__(self):

        self.extractor = DirectorDealingsExtractor()
        self.generator = InsiderSignalGenerator()
        self.notifier = TelegramNotifier()
        self.repository = InsiderSignalRepository()


    def process(
        self,
        announcement,
        documents,
    ):
        """
        Process insider dealing announcement.
        
        Returns:
            True if a notification was successfully sent
            False otherwise (no documents, extraction failed, not actionable, etc.)
        """

        if not documents:
            logging.warning(f"No documents provided for {announcement.announcement_id}")
            return False

        document = documents[0]
        logging.info(f"Processing director dealing document: {document.filename}")

        try:
            dealing = self.extractor.extract(
                announcement,
                document,
            )
        except Exception as e:
            logging.error(f"Failed to extract dealing from {document.filename}: {e}")
            return False
        
        logging.info(f"Director dealing extracted: {dealing.director_name if dealing else 'None'}")

        try:
            signal = self.generator.generate(dealing)
        except Exception as e:
            logging.error(f"Failed to generate signal: {e}")
            return False

        logging.info(f"Signal generated: {signal.signal}, Type: {signal.signal_type}")

        # Check if signal already exists (prevent duplicates)
        if self.repository.exists(signal.announcement_id):
            logging.warning(
                f"Signal already exists for announcement {signal.announcement_id}, skipping"
            )
            return False

        try:
            self.repository.insert(signal)
            logging.info(f"Signal stored: {signal.announcement_id}")
        except Exception as e:
            logging.error(f"Failed to store signal: {e}")
            return False

        # Only notify if signal is actionable
        if signal.signal:
            try:
                logging.info(f"Sending Telegram notification for {announcement.announcement_id}")
                self.notifier.notify(signal)
                logging.info(f"Notification sent successfully")
                return True  # Successfully sent detailed notification
            except Exception as e:
                logging.error(f"Failed to send Telegram notification: {e}")
                return False
        else:
            logging.debug(f"Signal not actionable, skipping notification")
            return False