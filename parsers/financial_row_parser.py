"""
Financial Row Parser

Converts one financial statement row
into structured numbers.
"""

import re


class FinancialRowParser:

    def _to_number(self, value):
        value = value.strip()

        if value in ("", "-", "N.M.", "N/M"):
            return None

        # Ignore accounting note references such as:
        # 4
        # 5
        # 7
        # 12
        # 4(a)
        if re.fullmatch(r"\d+(\([a-zA-Z]\))?", value):
            return None

        negative = False

        if value.startswith("(") and value.endswith(")"):
            negative = True
            value = value[1:-1]

        value = value.replace(",", "")

        try:
            number = float(value)

            if negative:
                number *= -1

            return number

        except ValueError:
            return None

    def parse(self, values):

        numbers = []

        for value in values:

            number = self._to_number(value)

            if number is not None:

                numbers.append(number)

        return {

            "current": numbers[0] if len(numbers) > 0 else None,

            "previous": numbers[1] if len(numbers) > 1 else None,

            "growth": numbers[2] if len(numbers) > 2 else None

        }