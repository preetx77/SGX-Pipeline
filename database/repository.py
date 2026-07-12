# Announcement Repository
# Contains all database operations related to announcements.


from datetime import datetime

from database.database import DatabaseManager
from models.announcement import Announcement


class AnnouncementRepository:

    def __init__(self):

        self.db = DatabaseManager()

    def announcement_exists(
        self,
        announcement_id: str
    ) -> bool:

        query = "SELECT 1 FROM announcements WHERE announcement_id = ?"
        row = self.db.fetchone(
            query,
            (announcement_id,)
        )
        return row is not None

    def insert(
        self,
        announcement: Announcement
    ):

        if self.announcement_exists(
            announcement.announcement_id
        ):
            return False

        now = datetime.utcnow().isoformat()

        query = """
        INSERT INTO announcements (
            announcement_id, ref_id, company_name, stock_code, isin_code,
            title, category, category_code, subcategory_code, announcement_url,
            submission_date, submission_timestamp, submitted_by, local_path,
            downloaded, parsed, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.db.execute(
            query,
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
                announcement.submission_date,
                announcement.submission_timestamp,
                announcement.submitted_by,
                None,
                0,
                0,
                now,
                now
            )
        )
        return True

    def close(self):
        self.db.close()

    def count(self) -> int:                 #    COUNT
        row = self.db.fetchone(
            """
            SELECT COUNT(*)
            FROM announcements
            """
        )
        return row[0]

    def get_latest(self):
        row = self.db.fetchone(
            """
            SELECT *
            FROM announcements
            ORDER BY submission_timestamp DESC 
            LIMIT 1
            """
        )
        return row

    # to get companny annoucnement 

    def get_company_announcement(
        self,
        stock_code: str
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
        return rows

    # -----------------to get by category 

    def get_by_category(
        self,
        category: str
    ):

        return self.db.fetchall(
        """
        SELECT *
        FROM announcements
        WHERE category = ?
        ORDER BY submission_timestamp DESC
        """,

        (category,)
    )