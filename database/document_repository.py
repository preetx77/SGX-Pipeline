from datetime import datetime

from database.database import DatabaseManager
from models.document import Document


class DocumentRepository:

    def __init__(self):

        self.db = DatabaseManager()

    # ---------------------------------------------------------
    # SQLite Row -> Document
    # ---------------------------------------------------------

    def _row_to_document(self, row):

        if row is None:
            return None

        from models.document_type import DocumentType

        return Document(

            attachment_id=row["attachment_id"],

            announcement_id=row["announcement_id"],

            announcement_title=row["announcement_title"],

            announcement_category=row["announcement_category"],

            company_name=row["company_name"],

            stock_code=row["stock_code"],

            filename=row["filename"],

            local_path=row["local_path"],

            text=row["extracted_text"],

            page_count=row["page_count"],

            word_count=row["word_count"],

            document_type=DocumentType(row["document_type"]),

            extracted=bool(row["extracted"])
        )
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

                document.word_count,

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
        return self._row_to_document(row)

    # --------------------------------------------------
    # Get documents by type
    # --------------------------------------------------

    def get_documents_by_type(self, document_type):

        rows = self.db.fetchall(
            """
            SELECT *
            FROM documents
            WHERE document_type = ?
            ORDER BY created_at DESC
            """,
            (document_type,)
        )

        return [
            self._row_to_document(row)
            for row in rows
        ]


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

    def get_financial_statements(self):
        """Get only actual financial statement documents, excluding press releases"""
        rows = self.db.fetchall(
            """
            SELECT *
            FROM documents
            WHERE document_type = ?
            AND (
                filename LIKE '%financial statement%'
                OR filename LIKE '%interim financial%'
                OR filename LIKE '%financial statements%'
            )
            ORDER BY created_at DESC
            """,
            ("Financial Results",)
        )
        
        return [self._row_to_document(row) for row in rows]

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(self):

        self.db.close()