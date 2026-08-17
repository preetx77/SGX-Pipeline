"""
Director Dealings Classifier

Converts raw SGX filing text into structured
transaction categories.

This is a rule-based classifier for now.
Later it can be upgraded to ML/LLM if needed.
"""




class DirectorDealingsClassifier:

    def classify(self, text: str):
        """
        Classify transaction type based on actual Form 1 structure.
        
        Key insights:
        1. TRANSACTION DIRECTION (Acquisition vs Disposal):
           - "Acquisition of:" with content = purchase/exercise
           - "Disposal of:" with content = sale/vesting
           - Empty disposal section = default to acquisition
        
        2. TRANSACTION TYPE (Market vs Corporate Action):
           - Item 6 "Amount of consideration" has filled SGD amount = MARKET_PURCHASE/MARKET_SELL
           - Item 6 empty = BONUS/RIGHTS/CORPORATE ACTION (no cash)
        
        3. OFF-MARKET detection:
           - Cannot reliably detect from text extraction (checkboxes not visible)
           - Default to MARKET for transactions with consideration
           - Text "off-market transaction" only appears in template, not selection
        """
        import re
        
        lower = text.lower()
        
        # Step 1: Determine if this is an acquisition (purchase) or disposal (sale)
        acquisition_sections = re.findall(
            r'Acquisition of:(.*?)(?:Disposal of:|Other circumstances|$)',
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        disposal_sections = re.findall(
            r'Disposal of:(.*?)(?:Other circumstances|Acceptance|$)',
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        has_acquisition = any(s.strip() and len(s.strip()) > 10 for s in acquisition_sections)
        has_disposal = any(s.strip() and len(s.strip()) > 10 for s in disposal_sections)
        
        is_disposal = has_disposal and not has_acquisition
        
        # Step 2: Check if there is a consideration amount (Item 6)
        # Look for both "S$" and plain "$" currency indicators
        consideration_match = re.search(
            r'Amount of consideration.*?[\$S][\$]?([\d,]+(?:\.\d{2})?)',
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        has_consideration = consideration_match is not None
        
        # Step 3: If there IS a consideration amount, this is a market transaction
        if has_consideration:
            # Default to MARKET for transactions with consideration
            # (OFF-MARKET cannot be reliably detected from text extraction)
            return "MARKET_SELL" if is_disposal else "MARKET_PURCHASE"
        
        # Step 4: If NO consideration amount, this is a corporate action
        # Use keywords to distinguish type
        
        # Bonus Issue
        if "bonus issue" in lower:
            return "BONUS_ISSUE"

        # Rights Issue
        if "rights issue" in lower:
            return "RIGHTS_ISSUE"

        # Share Award / Vesting
        if "share award" in lower or "vesting of share award" in lower:
            return "SHARE_AWARD"

        # Employee Share Option Exercise
        if "employee share option" in lower or "exercise of employee share option" in lower:
            return "OPTION_EXERCISE"

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