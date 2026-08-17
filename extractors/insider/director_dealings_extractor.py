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
        1. "Name of Individual:" (submitter, often the actual person/entity)
        2. Name on separate line immediately before "Name of Substantial Shareholder" (form variant, less common)
        3. "Name of Substantial Shareholder/Unitholder:" with actual name (primary pattern)
        
        Returns the name if found, None otherwise.
        """
        # Pattern 1 (PRIMARY): Fall back to Individual submitter name first (most reliable)
        match = re.search(
            r"Name of Individual:\s*\n\s*(.+?)(?:\n|$)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if match:
            name = match.group(1).strip()
            if name and not name.startswith("(") and len(name) > 2:
                return name
        
        # Pattern 2 (VARIANT): Form variant where shareholder name appears on its own line right before the label
        # But only try this if Pattern 1 returned nothing (i.e., name field is empty)
        # This catches cases like "Lim Sok Cheng Julie" or "Messiah Limited" on their own line
        match = re.search(
            r"\n([A-Za-z][^\n]*(?:Limited|Ltd|Fund|Corporation|Company)?)\nName of Substantial Shareholder/Unitholder:",
            text,
            flags=re.DOTALL
        )
        
        if match:
            name = match.group(1).strip()
            # Validate it's a real name, not form instruction
            if 3 < len(name) < 120 and not any(x in name.lower() for x in ['part', 'general', 'form', 'please', 'effective date', 'version']):
                return name
        
        # Pattern 3: Try to extract actual shareholder name with the primary pattern
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
        
        return None

    def extract_date(self, text):

        return self._extract_after_label(
        text,   
        "Date of acquisition of or change in interest:"
        )

    def extract_action(self, text):

        return None


    def extract_shares(self, text):
        """
        Extract number of shares from Form 1/Form 3.
        
        The form structure shows:
          5. Number of shares, units, rights, options, warrants...
             Exercise of 1,019,337 warrants to ordinary shares
          6. Amount of consideration...
        
        The actual count is in the description line, not the immediate next line.
        Need to extract the largest number in the "Number of shares" section.
        """
        import re
        
        # Find the "Number of shares" section, up to the next clause (e.g., "6. Amount")
        match = re.search(
            r"5\.\s*Number of shares.*?(?=\n\s*6\.|$)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if not match:
            return None
        
        section = match.group(0)
        
        # Find all numbers in this section (must have at least one digit, not just commas)
        # Pattern: one or more digits, optionally followed by comma-digit groups
        numbers = re.findall(r'\d{1,3}(?:,\d{3})*|\d+', section)
        
        if not numbers:
            return None
        
        # Filter: skip single/double digit numbers (clause numbers), 
        # return the first substantial number (100+)
        for num_str in numbers:
            try:
                num = int(num_str.replace(",", ""))
                if num >= 100:  # Likely a real count, not a clause number
                    return num
            except ValueError:
                # Skip malformed numbers
                continue
        
        # Fallback: if no large number found, return largest number found
        if numbers:
            try:
                return int(numbers[-1].replace(",", ""))
            except ValueError:
                pass
        
        return None

        

    def extract_price(self, text):
        """
        Extract transaction price per share from Form 1/Form 3.
        
        IMPORTANT: Only extracts UNIT PRICE (per-share prices).
        Total consideration amounts are NOT extracted here.
        
        Looks for patterns like:
        - "Price per share: SGD 0.50"
        - "Amount of consideration: S$1.31 per share"
        
        Note: "Amount of consideration: S$697,248.42" (without "per share") is NOT a unit price
        and should NOT be returned here. That value will be used directly as transaction value
        in the business logic, not multiplied by shares.
        """
        # Pattern 1: "Transaction price per share (SGD): X.XX" or "Price per share: ..."
        match = re.search(
            r"(?:Transaction price|Price).*?per share.*?:\s*(?:SGD|S\$)?\s*([\d.]+)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                pass
        
        # Pattern 2: "Amount of consideration: S$X.XX per share" (explicit per-share indicator)
        match = re.search(
            r"Amount of consideration.*?(?:S\$|SGD)\s*([\d.]+)\s*per share",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                pass
        
        # NOTE: Deliberately NOT including Pattern 3 that was matching bare S$ amounts
        # because that would capture total consideration (S$697,248.42) and treat it as a per-share price
        
        return None

    def extract_consideration_amount(self, text):
        """
        Extract total consideration amount (not per-share).
        
        This extracts total transaction amounts like:
        - "Amount of consideration: S$697,248.42" (total, not per-share)
        - Used when price per share is not available
        
        Returns the total amount if found, None otherwise.
        """
        # Match "Amount of consideration: S$XXX,XXX.XX" where it's NOT followed by "per share"
        # Can span multiple lines
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'Amount of consideration' in line:
                # Look ahead up to 3 lines to find the amount
                search_text = '\n'.join(lines[i:min(i+4, len(lines))])
                
                # Check if "per share" is present - if so, skip this
                if 'per share' in search_text.lower():
                    continue
                
                # Find currency amount
                match = re.search(
                    r"(?:S\$|SGD)\s*([\d,]+(?:\.\d{2})?)",
                    search_text,
                    flags=re.IGNORECASE
                )
                
                if match:
                    try:
                        return float(match.group(1).replace(",", ""))
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
        
        # Calculate value: shares * price if both available, otherwise use consideration amount
        value = None
        if shares is not None and price is not None:
            # Per-share price: value = shares * price
            value = shares * price
        elif shares is not None:
            # No per-share price: try to get total consideration amount
            consideration = self.extract_consideration_amount(text)
            if consideration is not None:
                value = consideration
        
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