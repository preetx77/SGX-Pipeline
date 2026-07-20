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

        return self._extract_after_label(
            text , "Name of Director/CEO:"
        )

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
        return None

    def extract(self, announcement, document):
        """
        Extract director dealing information from announcement and document.
        Returns a DirectorDealing object with extracted fields.
        """
        
        text = document.text if document else ""
        
        # Classify transaction type
        transaction_type = self.classifier.classify(text)
        
        return DirectorDealing(
            announcement_id=announcement.announcement_id,
            company_name=announcement.company_name,
            stock_code=announcement.stock_code,
            director_name=self.extract_director(text),
            transaction_type=transaction_type,
            action=self.classifier.action(transaction_type),
            importance=self.classifier.importance(transaction_type),
            shares=self.extract_shares(text),
            price=self.extract_price(text),
            value=None,  # Can be calculated from shares * price if needed
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