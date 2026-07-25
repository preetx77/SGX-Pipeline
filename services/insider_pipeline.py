from extractors.insider.director_dealings_extractor import ( DirectorDealingsExtractor)

from services.signals.insider_signal_generator import (InsiderSignalGenerator)

from notifications.telegram_notifier import (TelegramNotifier)
from database.insider_signal_repository import InsiderSignalRepository

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

        if not documents:
            print("No documents")
            return

        document = documents[0]
        print("✓ Document received")

        dealing = self.extractor.extract(
            announcement,
            document,
        )
        
        print("✓ Dealing extracted")

        signal = self.generator.generate(dealing)
        print("✓ Signal generated")

        print(signal)

        print("Exists:", self.repository.exists(signal.announcement_id))

        if not self.repository.exists(signal.announcement_id):
            print("Inserting...")
            self.repository.insert(signal)
            print("Inserted.")

        if signal.signal:
            print("Sending Telegram...")
            self.notifier.notify(signal)