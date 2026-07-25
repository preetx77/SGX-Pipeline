import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.database import DatabaseManager

db = DatabaseManager()

db.execute(
    """
    DELETE FROM announcements
    WHERE announcement_id = ?
    """,
    ("S42983PDNQ94SVRT",)
)

print("Announcement deleted.")