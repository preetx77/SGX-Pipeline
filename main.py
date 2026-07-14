from database.repository import AnnouncementRepository
from database.attachment_repository import AttachmentRepository
from database.document_repository import DocumentRepository

from extractors.pdf_extractor import PDFExtractor
from classifiers.document_classifier import DocumentClassifier

from models.attachment import Attachment


def main():

    announcement_repo = AnnouncementRepository()

    attachment_repo = AttachmentRepository()

    document_repo = DocumentRepository()

    extractor = PDFExtractor()

    classifier = DocumentClassifier()

    announcement = announcement_repo.get_latest()

    row = attachment_repo.db.fetchone("""

        SELECT *

        FROM attachments

        WHERE downloaded = 1

        LIMIT 1

    """)

    attachment = Attachment(

        attachment_id=row["attachment_id"],

        announcement_id=row["announcement_id"],

        filename=row["filename"],

        download_url=row["download_url"],

        local_path=row["local_path"],

        downloaded=bool(row["downloaded"])

    )

    document = extractor.extract(

        attachment,

        announcement

    )

    document.document_type = classifier.classify(document)

    inserted = document_repo.insert(document)

    print()

    print("=" * 70)

    print("Document Repository Test")

    print("=" * 70)

    print(f"Inserted : {inserted}")

    print(f"Type     : {document.document_type.value}")

    print(f"Words    : {document.word_count()}")

    print("=" * 70)

    announcement_repo.close()

    attachment_repo.close()

    document_repo.close()


if __name__ == "__main__":

    main()