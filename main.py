from database.announcement_repository import AnnouncementRepository
from database.attachment_repository import AttachmentRepository

from models.attachment import Attachment

from services.document_service import DocumentService


def main():

    announcement_repo = AnnouncementRepository()
    attachment_repo = AttachmentRepository()
    service = DocumentService()

    row = attachment_repo.get_downloaded_attachment()

    attachment = Attachment(

        attachment_id=row["attachment_id"],
        announcement_id=row["announcement_id"],
        filename=row["filename"],
        download_url=row["download_url"],
        local_path=row["local_path"],
        downloaded=bool(row["downloaded"])

    )

    announcement = announcement_repo.get_by_id(
        attachment.announcement_id
    )

    print()
    print("=" * 70)
    print("Relationship Check")
    print("=" * 70)

    print(f"Attachment Announcement ID : {attachment.announcement_id}")
    print(f"Announcement ID            : {announcement.announcement_id}")
    print(f"Company                    : {announcement.company_name}")
    print(f"Category                   : {announcement.category}")
    print(f"Title                      : {announcement.title}")
    print(f"Filename                   : {attachment.filename}")

    print("=" * 70)

    result = service.process(
        announcement,
        attachment
    )

    document = result["document"]

    print()
    print("=" * 70)
    print("Document Service")
    print("=" * 70)

    print(f"Predicted Type : {document.document_type.value}")
    print(f"Words          : {document.word_count()}")
    print(f"Inserted       : {result['inserted']}")

    print("=" * 70)

    service.close()
    announcement_repo.close()
    attachment_repo.close()


if __name__ == "__main__":
    main()