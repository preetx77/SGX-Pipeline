from database.document_repository import DocumentRepository

from extractors.insider.director_dealings_extractor import (
    DirectorDealingsExtractor,
)

from services.signals.insider_signal_generator import (
    InsiderSignalGenerator,
)

from notifications.telegram_notifier import (
    TelegramNotifier,
)


class SGXPipeline:

    def __init__(self):

        self.document_repo = DocumentRepository()
        self.extractor = DirectorDealingsExtractor()
        self.signal_generator = InsiderSignalGenerator()

    def process(self, announcement):

        documents = self.document_repo.get_documents_by_announcement(
            announcement.announcement_id
        )

        if not documents:
            return

        document = documents[0]

        dealing = self.extractor.extract(
            announcement,
            document,
        )

        signal = self.signal_generator.generate(
            dealing
        )

        return signal
        