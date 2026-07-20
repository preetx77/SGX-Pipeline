"""
Director Dealings Classifier

Converts raw SGX filing text into structured
transaction categories.

This is a rule-based classifier for now.
Later it can be upgraded to ML/LLM if needed.
"""




class DirectorDealingsClassifier:

    def classify(self, text: str):

        lower = text.lower()

        # Bonus Issue
        if "bonus issue" in lower:
            return "BONUS_ISSUE"

        # Rights Issue
        if "rights issue" in lower:
            return "RIGHTS_ISSUE"

        # Share Award
        if "share award" in lower:
            return "SHARE_AWARD"

        # Employee Share Option
        if "employee share option" in lower:
            return "OPTION_EXERCISE"

        # Off-market
        if "off-market transaction" in lower:

            if "disposal" in lower:
                return "OFF_MARKET_SELL"

            return "OFF_MARKET_PURCHASE"

        # Market transaction
        if "market transaction" in lower:

            if "disposal" in lower:
                return "MARKET_SELL"

            return "MARKET_PURCHASE"

        return "UNKNOWN"

    def action(self, transaction_type):

        mapping = {

            "MARKET_PURCHASE": "BUY",

            "MARKET_SELL": "SELL",

            "OFF_MARKET_PURCHASE": "BUY",

            "OFF_MARKET_SELL": "SELL",

            "BONUS_ISSUE": "BONUS",

            "RIGHTS_ISSUE": "RIGHTS",

            "SHARE_AWARD": "AWARD",

            "OPTION_EXERCISE": "EXERCISE",

            "UNKNOWN": "UNKNOWN"

        }

        return mapping.get(transaction_type, "UNKNOWN")

    def importance(self, transaction_type):

        importance = {

            "MARKET_PURCHASE": 10,

            "MARKET_SELL": 9,

            "OFF_MARKET_PURCHASE": 6,

            "OFF_MARKET_SELL": 5,

            "BONUS_ISSUE": 2,

            "RIGHTS_ISSUE": 3,

            "SHARE_AWARD": 3,

            "OPTION_EXERCISE": 4,

            "UNKNOWN": 0
        }

        return importance.get(transaction_type, 0)