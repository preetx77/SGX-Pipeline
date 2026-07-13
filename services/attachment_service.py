"""
Attachment Service
Coordinates parsing, persistence and downloading
for announcement attachments.
"""

from scraper.parser import AnnouncementParser
from scraper.downloader import PDFDownloader
from database.attachment_repository import AttachmentRepository


class AttachmentService:

    def __init__(self):
        self.parser = AnnouncementParser()
        self.downloader = PDFDownloader()
        self.repository = AttachmentRepository()

    def process_announcement(
        self,
        announcement
    ):

        attachments = self.parser.parse(announcement)
        discovered = len(attachments)
        inserted = 0
        downloaded = 0
        skipped = 0

        for attachment in attachments:
            is_new = self.repository.insert(
                attachment
            )
            if not is_new:
                skipped += 1
                continue
            inserted += 1

            path = self.downloader.download(
                attachment,
                announcement.stock_code,
                announcement.submission_date
            )

            self.repository.mark_downloaded(
                attachment.attachment_id,
                path
            )

            downloaded += 1
        return {
            "announcement": announcement.title,
            "attachments": discovered,
            "inserted": inserted,
            "downloaded": downloaded,
            "skipped": skipped
        }

    def close(self):
        self.repository.close()