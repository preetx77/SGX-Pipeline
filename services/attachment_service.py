"""
Attachment Service
Coordinates parsing, persistence and downloading
for announcement attachments.
"""

import logging
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
        logging.debug(f"Found {len(attachments)} attachments in {announcement.announcement_id}")
        
        new_attachments = []
        existing_attachments = []
        downloaded = []
        failed = []

        for attachment in attachments:
            is_new = self.repository.insert(
                attachment
            )
            if not is_new:
                # Get the attachment from database to check if it has been downloaded
                db_attachment = self.repository.get_by_id(
                    attachment.attachment_id
                )
                existing_attachments.append(db_attachment)
                
                # Also attempt to download existing attachments that don't have a path yet
                if not db_attachment.downloaded or db_attachment.local_path is None:
                    try:
                        logging.info(f"Re-downloading existing attachment {attachment.filename}")
                        path = self.downloader.download(
                            attachment,
                            announcement.stock_code,
                            announcement.submission_date
                        )

                        self.repository.mark_downloaded(
                            attachment.attachment_id,
                            path
                        )
                        
                        db_attachment.local_path = path
                        db_attachment.downloaded = True
                        downloaded.append(db_attachment)
                    except Exception as e:
                        logging.error(f"Failed to download {attachment.filename}: {e}")
                        failed.append({
                            "attachment": attachment,
                            "error": str(e)
                        })
                continue
            
            new_attachments.append(attachment)

            try:
                logging.info(f"Downloading new attachment {attachment.filename}")
                path = self.downloader.download(
                    attachment,
                    announcement.stock_code,
                    announcement.submission_date
                )

                self.repository.mark_downloaded(
                    attachment.attachment_id,
                    path
                )
                
                downloaded.append(attachment)
            except Exception as e:
                logging.error(f"Failed to download {attachment.filename}: {e}")
                failed.append({
                    "attachment": attachment,
                    "error": str(e)
                })

        if failed:
            logging.warning(f"{len(failed)} attachment(s) failed to download")

        return {
            "attachments": attachments,
            "new": new_attachments,
            "existing": existing_attachments,
            "downloaded": downloaded,
            "failed": failed
        }

    def close(self):
        self.repository.close()