"""
Statement Parser

Converts flattened PDF text into
a structured dictionary.
"""

import re


class StatementParser:

    ROWS = [

        "Revenue",

        "Cost of sales",

        "Gross profit",

        "Other income",

        "Other gains",

        "Other losses",

        "Profit before income tax",

        "Income tax expense",

        "Profit after income tax",

        "Basic and diluted earnings per share",

        "Cash and bank balances",

        "Trade and other receivables",

        "Inventories",

        "Total assets",

        "Trade and other payables",

        "Total liabilities",

        "Net assets"

    ]

    def parse(self, text):

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:

                lines.append(line)

        statement = {}

        i = 0

        while i < len(lines):

            current = lines[i]

            matched = False

            for row in self.ROWS:

                if current.lower().startswith(row.lower()):

                    values = []

                    j = i + 1

                    while j < len(lines):

                        nxt = lines[j]

                        if any(
                            nxt.lower().startswith(r.lower())
                            for r in self.ROWS
                        ):
                            break

                        values.append(nxt)

                        j += 1

                    statement[row] = values

                    i = j

                    matched = True

                    break

            if not matched:

                i += 1

        return statement