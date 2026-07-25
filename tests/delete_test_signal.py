import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.database import DatabaseManager

db = DatabaseManager()

db.execute(
    """
    DELETE FROM insider_signals
    WHERE announcement_id = ?
    """,
    ("TEST123456",)
)

print("Deleted.")