import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.database import DatabaseManager

db = DatabaseManager()

rows = db.fetchall("""
SELECT *
FROM insider_signals
""")

for row in rows:
    print(dict(row))