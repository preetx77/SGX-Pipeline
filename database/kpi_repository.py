from datetime import datetime
from database.database import DatabaseManager
from models.financial_metric import FinancialMetric

class KPIRepository:

    def __init__(self):
        self.db = DatabaseManager()

    # --------------------------------------------------

    def insert(self, metric):
        if self.exists(metric):
            return False
            
        self.db.execute(
            """
            INSERT INTO financial_metrics(
                announcement_id,
                stock_code,
                company_name,
                metric_name,
                metric_value,
                reporting_period,
                currency,
                created_at
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,

            (
                metric.announcement_id,
                metric.stock_code,
                metric.company_name,
                metric.metric_name,
                metric.current_value,
                metric.reporting_period,
                metric.currency,
                datetime.utcnow().isoformat()
            )
        )
        return True
    # --------------------------------------------------

    def get_company_metrics(
        self,
        stock_code,
        metric_name
    ):
        return self.db.fetchall(
            """
            SELECT *
            FROM financial_metrics
            WHERE
                stock_code=?
            AND
                metric_name=?
            ORDER BY id
            """,
            (
                stock_code,
                metric_name
            )
        )
    # --------------------------------------------------

    def count(self):
        row = self.db.fetchone(
            """
            SELECT COUNT(*)
            FROM financial_metrics
            """
        )
        return row[0]

    # --------------------------------------------------

    def close(self):
        self.db.close()

    # --------------------------------------------

    def exists(self, metric):
        row = self.db.fetchone(
            """
            SELECT 1
            FROM financial_metrics
            WHERE
                announcement_id = ?
            AND
                metric_name = ?
            """,
            (
                metric.announcement_id,
                metric.metric_name
            )
        )
        return row is not None

# ------------------------------------------------------
    def get_latest_metric(self, stock_code, metric_name):

        row = self.db.fetchone(
            """
            SELECT * 
            
            FROM financial_metrics
            WHERE
                stock_code = ?
            AND
                metric_name = ?
            ORDER BY id DESC
            LIMIT 1
            """, 
            (stock_code, metric_name)
        )
        return self._row_to_model(row)

    # ----------------------------------------------------

    def get_previous_metric(
        self, stock_code, metric_name
    ):

        row = self.db.fetchone(
            """
            SELECT * 
            FROM financial_metrics
            WHERE
                stock_code = ?
            AND
                metric_name = ?
            ORDER BY id DESC
            LIMIT 1 OFFSET 1
            """,
            (stock_code, metric_name)
        )
    
        return self._row_to_model(row)

# ------------------------------------------------
    def _row_to_model(self, row):

        if row is None:
            return None

        return FinancialMetric(
            announcement_id = row["announcement_id"],
            company_name = row["company_name"],
            stock_code = row["stock_code"],
            metric_name = row["metric_name"],
            current_value = row["metric_value"],
            reporting_period = row["reporting_period"],
            currency = row["currency"]
        )