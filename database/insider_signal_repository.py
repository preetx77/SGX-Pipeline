from database.database import DatabaseManager


class InsiderSignalRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def insert(self, signal):

        query = """
        INSERT INTO insider_signals (

            announcement_id,
            company_name,
            stock_code,
            signal,
            signal_type,
            direction,
            decision,
            confidence,
            shares,
            price,
            value,
            direct_interest_before,
            direct_interest_after,
            created_at

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.db.execute(
            query,
            (
                signal.announcement_id,
                signal.company_name,
                signal.stock_code,
                int(signal.signal),
                signal.signal_type,
                signal.direction,
                signal.decision,
                signal.confidence,
                signal.shares,
                signal.price,
                signal.value,
                signal.direct_interest_before,
                signal.direct_interest_after,
                signal.created_at
            )
        )

    def exists(self, announcement_id):

        query = """
        SELECT 1
        FROM insider_signals
        WHERE announcement_id = ?
        LIMIT 1
        """

        return self.db.fetchone(
            query,
            (announcement_id,)
        ) is not None

    def latest(self, stock_code):

        query = """
        SELECT *
        FROM insider_signals
        WHERE stock_code = ?
        ORDER BY created_at DESC
        LIMIT 1
        """

        return self.db.fetchone(query, (stock_code,))

    def get_all(self):

        query = """
        SELECT *
        FROM insider_signals
        ORDER BY created_at DESC
        """

        return self.db.fetchall(query)

    def close(self):
        """Close database connection"""
        self.db.close()