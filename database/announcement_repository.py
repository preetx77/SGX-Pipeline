from models.announcement import Announcement
from database.database import DatabaseManager


class AnnouncementRepository:

    def __init__(self):

        self.db = DatabaseManager()

    # --------------------------------------------------
    # Check if announcement exists
    # --------------------------------------------------

    def exists(self, announcement_id):

        row = self.db.fetchone(

            """
            SELECT 1

            FROM announcements

            WHERE announcement_id = ?

            """,

            (announcement_id,)

        )

        return row is not None

    # --------------------------------------------------
    # Insert announcement
    # --------------------------------------------------

    def insert(self, announcement):

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
                submission_date

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                announcement.submission_date

            )

        )

    # --------------------------------------------------
    # Convert SQLite Row -> Announcement object
    # --------------------------------------------------

    def _row_to_announcement(self, row):

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

    # --------------------------------------------------
    # Get announcement by ID
    # --------------------------------------------------

    def get_by_id(self, announcement_id):

        row = self.db.fetchone(

            """
            SELECT *

            FROM announcements

            WHERE announcement_id = ?

            """,

            (announcement_id,)

        )

        return self._row_to_announcement(row)

    # --------------------------------------------------
    # Latest announcement
    # --------------------------------------------------

    def get_latest(self):

        row = self.db.fetchone(

            """
            SELECT *

            FROM announcements

            ORDER BY submission_timestamp DESC

            LIMIT 1
            """

        )

        return self._row_to_announcement(row)

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    def count(self):

        row = self.db.fetchone(

            """
            SELECT COUNT(*)

            FROM announcements
            """

        )

        return row[0]

    # --------------------------------------------------
    # Company announcements
    # --------------------------------------------------

    def get_company_announcements(self, stock_code):

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

            self._row_to_announcement(row)

            for row in rows

        ]

    # -------------------------------------------------

    def get_announcements_by_category(self, stock_code, category):

        rows = self.db.fetchall(
            """
            SELECT *
            FROM announcements
            WHERE
                stock_code = ?
            AND
                category = ?
            ORDER BY submission_timestamp DESC
            """,
            (stock_code, category)
        )
        
        return [
            self._row_to_announcement(row)
            for row in rows
        ]

    # --------------------------------------------------

    def close(self):

        self.db.close()

    # ------------------------------------------------
    