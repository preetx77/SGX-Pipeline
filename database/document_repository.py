from datetime import datetime

from database.database import DatabaseManager
from models.document import Document


class DocumentRepository:

    def __init__(self):

        self.db = DatabaseManager()

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def exists(self, attachment_id: str):

        row = self.db.fetchone(

            """
            SELECT 1
            FROM documents
            WHERE attachment_id = ?
            """,

            (attachment_id,)
        )

        return row is not None

    # ---------------------------------------------------------
    # Insert
    # ---------------------------------------------------------

    def insert(self, document: Document):

        if self.exists(document.attachment_id):
            return False

        now = datetime.utcnow().isoformat()

        self.db.execute(

            """
            INSERT INTO documents (

                attachment_id,

                announcement_id,

                company_name,

                stock_code,

                announcement_title,

                announcement_category,

                filename,

                local_path,

                page_count,

                word_count,

                document_type,

                extracted,

                extracted_text,

                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (

                document.attachment_id,

                document.announcement_id,

                document.company_name,

                document.stock_code,

                document.announcement_title,

                document.announcement_category,

                document.filename,

                document.local_path,

                document.page_count,

                document.word_count(),

                document.document_type.value,

                int(document.extracted),

                document.text,

                now

            )

        )

        return True

    # ---------------------------------------------------------
    # Count
    # ---------------------------------------------------------

    def count(self):

        row = self.db.fetchone(

            """
            SELECT COUNT(*)
            FROM documents
            """
        )

        return row[0]

    # ---------------------------------------------------------
    # Latest
    # ---------------------------------------------------------

    def latest(self):

        return self.db.fetchone(

            """
            SELECT *

            FROM documents

            ORDER BY created_at DESC

            LIMIT 1
            """
        )

    # ---------------------------------------------------------
    # By Type
    # ---------------------------------------------------------

    def get_by_type(self, document_type):

        return self.db.fetchall(

            """
            SELECT *

            FROM documents

            WHERE document_type = ?

            ORDER BY created_at DESC
            """,

            (document_type,)
        )

    # ---------------------------------------------------------
    # By Company
    # ---------------------------------------------------------

    def get_company_documents(

        self,

        stock_code

    ):

        return self.db.fetchall(

            """
            SELECT *

            FROM documents

            WHERE stock_code = ?

            ORDER BY created_at DESC
            """,

            (stock_code,)
        )

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(self):

        self.db.close()