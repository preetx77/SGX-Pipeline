import re

from models.director_dealing import DirectorDealing
from classifiers.director_dealings_classifier import DirectorDealingsClassifier


class DirectorDealingsExtractor:

    def __init__(self):
        """Initialize with classifier for transaction type detection."""
        self.classifier = DirectorDealingsClassifier()

    def _extract_after_label(self, text: str, label: str):
        """
        Extract the first non-empty, non-numeric line after a label.
        
        Handles formats like:
            Name of Director/CEO:
            3.
            Yong Khai Weng
            4.
        """
        pattern = rf"{re.escape(label)}(.*?)(?:\n\n|\Z)"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if not match:
            return None

        block = match.group(1)
        lines = []

        for line in block.splitlines():
            line = line.strip()

            if not line:
                continue

            # Ignore numbering like "3." or "10."
            if re.fullmatch(r"\d+\.", line):
                continue

            lines.append(line)

        if not lines:
            return None

        return lines[0]


    def extract_direct_interest_after(self, text):

        match = re.search(

            r"Immediately after.*?No\. of ordinary voting shares/units held:\s*([\d,]+)",

            text,

            flags=re.DOTALL | re.IGNORECASE

        )

        if not match:
            return None

        return int(
            match.group(1).replace(",", "")
        )

    def extract_director(self, text):
        """
        Extract director name from Form 1/eFORM1.
        Returns the director name if found, None otherwise.
        """
        return self._extract_after_label(
            text , "Name of Director/CEO:"
        )

    def extract_substantial_shareholder(self, text):
        """
        Extract substantial shareholder name from Form 3/eFORM3.
        
        Tries patterns in order:
        1. "Name of Substantial Shareholder/Unitholder:" with actual name (not blank/checkbox)
        2. "Name of Individual:" (submitter on behalf of shareholder)
        
        Returns the name if found, None otherwise.
        """
        # Pattern 1: Try to extract actual shareholder name
        # Look for the label and then the first real name-like line (skip checkboxes)
        match = re.search(
            r"Name of Substantial Shareholder/Unitholder:\s*\n\s*\d+\.\s*\n\s*(.+?)(?:\n|$)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if match:
            name = match.group(1).strip()
            # Skip if it's a checkbox/form instruction, not a real name
            if name and not name.startswith("Is ") and len(name) > 3:
                return name
        
        # Pattern 2: Fall back to Individual submitter name
        match = re.search(
            r"Name of Individual:\s*\n\s*(.+?)(?:\n|$)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if match:
            name = match.group(1).strip()
            if name and not name.startswith("(") and len(name) > 2:
                return name
        
        return None

    def extract_date(self, text):

        return self._extract_after_label(
        text,   
        "Date of acquisition of or change in interest:"
        )

    def extract_action(self, text):

        return None


    def extract_shares(self, text):

        match = re.search(
            r"Number of shares.*?\n([\d,]+)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if not match:
            return None

        return int(
            match.group(1).replace(",", "")
        )

        

    def extract_price(self, text):
        """
        Extract transaction price from Form 1/Form 3.
        
        Looks for patterns like:
        - "Transaction price per share (SGD): 0.50"
        - "Price per share: SGD 0.50"
        - Pattern: any variation with SGD and a decimal number
        """
        # Pattern 1: "Transaction price per share (SGD): X.XX" or similar
        match = re.search(
            r"(?:Transaction price|Price).*?(?:per share)?.*?:\s*(?:SGD\s*)?([\d.]+)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                pass
        
        # Pattern 2: "SGD 0.50" or "SGD0.50"
        match = re.search(
            r"SGD\s*([\d.]+)",
            text,
            flags=re.IGNORECASE
        )
        
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                pass
        
        return None

    def extract(self, announcement, document):
        """
        Extract director dealing information from announcement and document.
        Returns a DirectorDealing object with extracted fields.
        """
        
        text = document.text if document else ""

        print("\n" + "=" * 100)
        print("DIRECTOR DEALINGS PDF")
        

        # Classify transaction type
        transaction_type = self.classifier.classify(text)
        
        # Extract fields
        shares = self.extract_shares(text)
        price = self.extract_price(text)
        
        # Calculate value: shares * price if both available
        value = None
        if shares is not None and price is not None:
            value = shares * price
        
        return DirectorDealing(
            announcement_id=announcement.announcement_id,
            company_name=announcement.company_name,
            stock_code=announcement.stock_code,
            director_name=self.extract_director(text),
            transaction_type=transaction_type,
            action=self.classifier.action(transaction_type),
            importance=self.classifier.importance(transaction_type),
            shares=shares,
            price=price,
            value=value,
            currency="SGD",  # Default to SGD for SGX listings
            dealing_date=self.extract_date(text),
            direct_interest_before = self.extract_direct_interest_before(text),
            direct_interest_after = self.extract_direct_interest_after(text)
        )

    def extract_direct_interest_before(self, text):

        match = re.search(

            r"Immediately before.*?No\. of ordinary voting shares/units held:\s*([\d,]+)",

            text,

            flags=re.DOTALL | re.IGNORECASE

        )

        if not match:
            return None

        return int(
            match.group(1).replace(",", "")
        )