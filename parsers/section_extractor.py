"""
Section Extractor

Extracts only the financial statement
sections from a PDF.
"""


class SectionExtractor:

    START_KEYWORDS = [
        "A. CONDENSED INTERIM STATEMENT OF COMPREHENSIVE INCOME",
        "A. STATEMENT OF COMPREHENSIVE INCOME",
        "STATEMENT OF COMPREHENSIVE INCOME",
        "CONDENSED INTERIM CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME",
        "CONDENSED CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME"
    ]

    END_KEYWORDS = [
        "B. CONDENSED INTERIM BALANCE SHEETS",
        "B. BALANCE SHEETS",
        "BALANCE SHEETS",
        "CONDENSED INTERIM BALANCE SHEETS",
        "STATEMENT OF FINANCIAL POSITION"
    ]

    def income_statement(self, text):

        start = -1

        for keyword in self.START_KEYWORDS:

            pos = text.upper().find(keyword.upper())

            if pos != -1:

                start = pos

                break

        if start == -1:

            return ""

        end = len(text)

        for keyword in self.END_KEYWORDS:

            pos = text.upper().find(keyword.upper(), start)

            if pos != -1:

                end = pos

                break

        return text[start:end]
