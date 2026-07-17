from database.announcement_repository import AnnouncementRepository
from services.attachment_service import AttachmentService
from services.document_service import DocumentService


class HistoricalProcessingService:

    def __init__(self):
        self.announcement_repo = AnnouncementRepository()
        self.attachment_service = AttachmentService()
        self.document_service = DocumentService()

    def process_company(self, stock_code):

        announcements = self.announcement_repo.get_company_announcements(stock_code)

        print(f"Processing {len(announcements)} announcements")
        for announcement in announcements:
            self.process_announcement(announcement)

    def process_announcement(self, announcement):
        print(f"\n{announcement.submission_date} | {announcement.title}")

        result = self.attachment_service.process_announcement(announcement)
        
        print(f"  Attachments discovered: {len(result['attachments'])}")
        print(f"  New: {len(result['new'])}, Existing: {len(result['existing'])}, Downloaded: {len(result['downloaded'])}")
        
        # Process newly downloaded attachments through document service
        for attachment in result["downloaded"]:
            response = self.document_service.process(announcement, attachment)
            document = response["document"]
            print(f"    + {attachment.filename} -> {document.document_type}")
        
        # Also process already-downloaded attachments that don't have documents yet
        for attachment in result["existing"]:
            if attachment.downloaded and attachment.local_path:
                # Check if document already exists for this attachment
                if not self.document_service.repository.exists(attachment.attachment_id):
                    response = self.document_service.process(announcement, attachment)
                    document = response["document"]
                    print(f"    + {attachment.filename} -> {document.document_type} (cached)")
        
        # Log any download failures
        for failure in result["failed"]:
            print(f"    - {failure['attachment'].filename} (Error: {failure['error']})")

        