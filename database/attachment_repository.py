# need repo for attachment 
# Not because we need it immediately, but because we're following the same architecture as announcements.

from datetime import datetime
from database.database import DatabaseManager
from models.attachment import Attachment


class AttachmentRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def exists(
        self,
        attachment_id: str
    ):

        row = self.db.fetchone(
            """
            SELECT 1

            FROM attachments

            WHERE attachment_id = ?
            """,
            (attachment_id,)
        )

        return row is not None

    def insert(
        self,
        attachment: Attachment
    ):

        if self.exists(
            attachment.attachment_id
        ):
            return False

        now = datetime.utcnow().isoformat()

        self.db.execute(

            """
            INSERT INTO attachments (

                attachment_id,

                announcement_id,

                filename,

                download_url,

                file_size,

                local_path,

                downloaded,

                created_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (

                attachment.attachment_id,
                attachment.announcement_id,
                attachment.filename,
                attachment.download_url,
                attachment.file_size,
                attachment.local_path,
                int(attachment.downloaded),
                now
            )
        )

        return True

    def close(self):

        self.db.close()

# after downoading pdf we need to record : dowload= true and file loction 

    def mark_downloaded(
    self,
    attachment_id: str,
    local_path: str
    ):

        self.db.execute(
            """
            UPDATE attachments

            SET
                downloaded = 1,
                local_path = ?

            WHERE attachment_id = ?
            """,

            (
                local_path,
                attachment_id
        )
    )

    def get_downloaded_attachment(self):

        row = self.db.fetchone(
            """
            SELECT *

            FROM attachments

            WHERE downloaded = 1

            LIMIT 1
            """
        )

        return row

    def get_by_id(self, attachment_id: str):
        """Retrieve attachment by ID"""
        row = self.db.fetchone(
            """
            SELECT *
            FROM attachments
            WHERE attachment_id = ?
            """,
            (attachment_id,)
        )
        
        if row is None:
            return None
        
        return self._row_to_attachment(row)
    
    def _row_to_attachment(self, row):
        """Convert database row to Attachment object"""
        from models.attachment import Attachment
        
        return Attachment(
            attachment_id=row[0],
            announcement_id=row[1],
            filename=row[2],
            download_url=row[3],
            file_size=row[4],
            local_path=row[5],
            downloaded=bool(row[6])
        )