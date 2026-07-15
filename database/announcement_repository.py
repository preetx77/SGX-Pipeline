from datetime import datetime

from database.database import DatabaseManager
from models.announcement import Announcement


class AnnouncementRepository:

    def __init__(self):

        self.db = DatabaseManager()

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def exists(self, announcement_id: str):

        row = self.db.fetchone(

            """
            SELECT 1
            FROM announcements
            WHERE announcement_id = ?
            """,

            (announcement_id,)
        )

        return row is not None

    # ---------------------------------------------------------
    # Insert
    # ---------------------------------------------------------

    def insert(self, announcement: Announcement):

        if self.exists(announcement.announcement_id):
            return False

        now = datetime.utcnow().isoformat()

        self.db.execute(

            """
            INSERT INTO announcements (

                announcement_id,
                ref_id,

                company_name,
                stock_code,
                isin_code,

                title,

                category,
                category_code,
                subcategory_code,

                announcement_url,

                submission_timestamp,
                submission_date,

                local_path,

                downloaded,

                parsed,

                scraped_at

            )

            VALUES
            (
                ?,?,?,?,?,?,
                ?,?,?,?,
                ?,?,?,?,
                ?,?
            )
            """,

            (

                announcement.announcement_id,

                announcement.ref_id,

                announcement.company_name,

                announcement.stock_code,

                announcement.isin_code,

                announcement.title,

                announcement.category,

                announcement.category_code,

                announcement.subcategory_code,

                announcement.announcement_url,

                announcement.submission_timestamp,

                announcement.submission_date,

                announcement.local_path,

                int(announcement.downloaded),

                int(announcement.parsed),

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
            FROM announcements
            """
        )

        return row[0]

    # ---------------------------------------------------------
    # Latest
    # ---------------------------------------------------------

    def get_latest(self):

        row = self.db.fetchone(

            """
            SELECT *
            FROM announcements
            ORDER BY submission_timestamp DESC
            LIMIT 1
            """
        )

        return self._row_to_model(row)

    # ---------------------------------------------------------
    # Latest timestamp
    # ---------------------------------------------------------
    # -------------------------------------------------------
    # Get by ID
    # -------------------------------------------------------

    def get_by_id(self, announcement_id):

        row = self.db.fetchone(

            """
            SELECT *

            FROM announcements

            WHERE announcement_id = ?

            """,

            (announcement_id,)

        )

        if row is None:

            return None

        return self._row_to_model(row)


    def get_latest_timestamp(

        self,

        stock_code

    ):

        row = self.db.fetchone(

            """
            SELECT submission_date

            FROM announcements

            WHERE stock_code = ?

            ORDER BY submission_timestamp DESC

            LIMIT 1
            """,

            (stock_code,)
        )

        if row:

            return row["submission_date"]

        return None

    # ---------------------------------------------------------
    # Company announcements
    # ---------------------------------------------------------

    def get_company_announcements(

        self,

        stock_code

    ):

        rows = self.db.fetchall(

            """
            SELECT *

            FROM announcements

            WHERE stock_code = ?

            ORDER BY submission_timestamp DESC
            """,

            (stock_code,)
        )

        return [

            self._row_to_model(row)

            for row in rows

        ]

    # ---------------------------------------------------------
    # Row → Model
    # ---------------------------------------------------------

    def _row_to_model(

        self,

        row

    ):

        if row is None:

            return None

        return Announcement(

            announcement_id=row["announcement_id"],
            ref_id=row["ref_id"],
            company_name=row["company_name"],
            stock_code=row["stock_code"],
            isin_code=row["isin_code"],
            title=row["title"],
            category=row["category"],
            category_code=row["category_code"],
            subcategory_code=row["subcategory_code"],
            announcement_url=row["announcement_url"],
            submission_timestamp=row["submission_timestamp"],
            submission_date=row["submission_date"],
            submitted_by=row["submitted_by"]
        )

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(self):

        self.db.close()