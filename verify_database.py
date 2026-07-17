from database.database import DatabaseManager

db = DatabaseManager()

rows = db.fetchall("PRAGMA table_info(documents)")

for row in rows:
    print(row)