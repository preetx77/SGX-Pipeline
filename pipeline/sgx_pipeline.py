from database.document_repository import DocumentRepository

from extractors.insider.director_dealings_extractor import (
    DirectorDealingsExtractor,
)

from services.signals.insider_signal_generator import (
    InsiderSignalGenerator,
)

from pipeline.announcement_router import (
    AnnouncementRouter,
)


class SGXPipeline:

    def __init__(self):

        self.document_repo = DocumentRepository()
        self.extractor = DirectorDealingsExtractor()
        self.signal_generator = InsiderSignalGenerator()

    def process(self, announcement):

        print("=" * 60)
        print(f"Company   : {announcement.company_name}")
        print(f"Category  : {announcement.category}")
        print(f"Title     : {announcement.title}")

        if not AnnouncementRouter.is_insider(announcement):
            print("Router    : SKIPPED")
            return None

        print("Router    : PASSED")

        documents = self.document_repo.get_documents_by_announcement(
            announcement.announcement_id
        )

        print(f"Documents : {len(documents)}")

        if not documents:
            print("[Pipeline] No documents found.")
            return None

        document = documents[0]

        # Step 3 : Extract
        dealing = self.extractor.extract(
            announcement,
            document,
        )

        # Step 4 : Generate Signal
        signal = self.signal_generator.generate(
            dealing
        )

        return signal