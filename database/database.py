# this file should never know sgx exists, only job is to SQLITE
# if we move from SQLITE to POSTGRE : only this file changes


import sqlite3
import logging
from pathlib import Path

class DatabaseManager:

    def __init__(self):
        
        root = Path(__file__).parent
        self.db_path = root / "database.db"

        try:
            self.connection = sqlite3.connect(
                self.db_path,
                timeout=10.0,  # Wait up to 10 seconds for locks
                check_same_thread=False  # Allow use from different threads
            )
            self.connection.row_factory = sqlite3.Row 
            self.connection.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for better concurrency
            self.cursor = self.connection.cursor()
            logging.info(f"Database connection established: {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"Failed to connect to database: {e}")
            raise
        
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables if they don't exist"""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            try:
                with open(schema_path, 'r') as f:
                    schema = f.read()
                    self.cursor.executescript(schema)
                    self.connection.commit()
                    logging.info("Database schema initialized")
            except sqlite3.Error as e:
                logging.error(f"Failed to initialize database schema: {e}")
                raise
        else:
            logging.warning(f"Schema file not found: {schema_path}")

    def execute(
        self, 
        query,
        parameters = ()
    ):
        """Execute a query with error handling"""
        try:
            self.cursor.execute(query, parameters)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            logging.error(f"Database operational error: {e}")
            # Try to recover by reopening connection
            self._reconnect()
            raise
        except sqlite3.Error as e:
            logging.error(f"Database error executing query: {e}")
            raise

    def fetchone(
        self,
        query,
        parameters=()
    ):
        """Fetch one row with error handling"""
        try:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Database error fetching one row: {e}")
            raise

    def fetchall(
            self,
            query,
            parameters=()
    ):
        """Fetch all rows with error handling"""
        try:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Database error fetching all rows: {e}")
            raise

    def _reconnect(self):
        """Attempt to reconnect to database"""
        try:
            logging.warning("Attempting to reconnect to database...")
            if self.connection:
                self.connection.close()
            self.connection = sqlite3.connect(
                self.db_path,
                timeout=10.0,
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA journal_mode=WAL")
            self.cursor = self.connection.cursor()
            logging.info("Successfully reconnected to database")
        except Exception as e:
            logging.error(f"Failed to reconnect to database: {e}")
            raise

    def close(self):
        """Close database connection"""
        try:
            if self.connection:
                self.connection.close()
                logging.info("Database connection closed")
        except Exception as e:
            logging.warning(f"Error closing database connection: {e}")

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
        try:
            row = self.fetchone(query, (stock_code,))
            if row is None:
                return None
            return row[0]
        except Exception as e:
            logging.error(f"Failed to get latest timestamp for {stock_code}: {e}")
            raise
