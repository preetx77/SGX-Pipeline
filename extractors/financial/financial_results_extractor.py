"""
Financial Results Extractor

Extracts structured KPIs from
Financial Results documents.
"""

import re

from models.financial_result import FinancialResult
from extractors.base_extractor import BaseExtractor

class FinancialResultsExtractor(BaseExtractor):

    def extract(self, document):

        result = FinancialResult(
            announcement_id=document.announcement_id,
            company_name=document.company_name,
            stock_code=document.stock_code,
            extracted=False
        )

        text = document.text

        # --------------------------------------------------
        # Currency
        # --------------------------------------------------

        currency = re.search(
            r"\b(SGD|USD|RM|MYR)\b",
            text
        )

        if currency:
            result.currency = currency.group(1)

        # --------------------------------------------------
        # Reporting Period
        # --------------------------------------------------

        period = re.search(
            r"(Q[1-4]\s*FY\d{4})",
            text,
            re.IGNORECASE
        )

        if period:
            result.reporting_period = period.group(1)

        # --------------------------------------------------
        # Revenue
        # --------------------------------------------------

        revenue = re.search(
            r"Revenue\s*[:\-]?\s*([\d,]+\.\d+|[\d,]+)",
            text,
            re.IGNORECASE
        )

        if revenue:
            result.revenue = float(
                revenue.group(1).replace(",", "")
            )

        # --------------------------------------------------
        # Net Profit
        # --------------------------------------------------

        profit = re.search(
            r"Net Profit\s*[:\-]?\s*([\d,]+\.\d+|[\d,]+)",
            text,
            re.IGNORECASE
        )

        if profit:
            result.net_profit = float(
                profit.group(1).replace(",", "")
            )

        result.extracted = True
        return result