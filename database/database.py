# this file should never know sgx exists, only job is to SQLITE
# if we move from SQLITE to POSTGRE : only this file changes


import sqlite3
from pathlib import Path

class DatabaseManager:

    def __init__(self):
        
        root = Path(__file__).parent
        self.db_path = root / "database.db"

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row 
        self.cursor = self.connection.cursor()
        
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables if they don't exist"""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = f.read()
                self.cursor.executescript(schema)
                self.connection.commit()

    def execute(
        self, 
        query,
        parameters = ()
    ):
        self.cursor.execute(
            query,
            parameters
        )

        self.connection.commit()

    def fetchone(
        self,
        query,
        parameters=()
    ):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchone()

    def fetchall(
            self,
            query,
            parameters=()
    ):

        self.cursor.execute(
            query,
            parameters
        )

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

# ----------------- Incremental Synchronization ------------ 

    def get_latest_timestamp(self, stock_code: str) -> int | None:
        """
        Returns the newest submission timestamp
        for a company.
        """
        query = """
            SELECT submission_timestamp
            FROM announcements
            WHERE stock_code = ?
            ORDER BY submission_timestamp DESC
            LIMIT 1
        """
        row = self.fetchone(query, (stock_code,))
        if row is None:
            return None
        return row[0]
