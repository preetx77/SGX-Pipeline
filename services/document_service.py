
# Document Service : Coordinates document extraction, classification and storage.


from extractors.pdf_extractor import PDFExtractor
from classifiers.document_classifier import DocumentClassifier
from database.document_repository import DocumentRepository


class DocumentService:

    def __init__(self):

        self.extractor = PDFExtractor()
        self.classifier = DocumentClassifier()
        self.repository = DocumentRepository()

    def process(
        self,
        announcement,
        attachment
    ):

        # Extract PDF
        document = self.extractor.extract(attachment, announcement)

        print("\n Debug")
        print("title :" , document.announcement_title)
        print("Categoty :", document.announcement_category)

        document.document_type = self.classifier.classify(document)

        # Save
        inserted = self.repository.insert(
            document
        )

        return {
            "document": document,
            "inserted": inserted
        }

    def close(self):
        self.repository.close()