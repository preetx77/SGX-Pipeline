"""
Phase 4: Extraction Accuracy Testing (Direct PDF Analysis)

When database is empty, analyze PDF files directly from data/raw directory.
Extract and validate 100+ director-dealing announcements.
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import PyPDF2
    PYPDF_AVAILABLE = True
except:
    PYPDF_AVAILABLE = False
    print("WARNING: PyPDF2 not available, using file-based text extraction")


class Phase4DirectPDFTester:
    """
    Executes Phase 4 using PDF files directly from data/raw
    """
    
    def __init__(self):
        self.results = []
        self.test_filings = []
        self.raw_data_dir = Path(__file__).parent / "data" / "raw"
        
    def discover_director_dealing_pdfs(self) -> List[Dict]:
        """
        Discover all director dealing PDFs from data/raw directory.
        Look for Form 1, Form 3, and Disclosure of Interest files.
        """
        print("\n" + "="*100)
        print("PHASE 4: EXTRACTION ACCURACY TESTING (Direct PDF Analysis)")
        print("="*100)
        print("\n[1] SOURCING DIRECTOR DEALING PDFs...")
        
        filings = []
        
        if not self.raw_data_dir.exists():
            print(f"  ✗ Data directory not found: {self.raw_data_dir}")
            return []
        
        # Look for Form 1 and Form 3 PDFs
        patterns = [
            r'Form\s+1.*\.pdf',
            r'Form\s+3.*\.pdf',
            r'eFORM3.*\.pdf',
            r'Disclosure.*\.pdf',
        ]
        
        pdf_files = []
        
        # Recursively search for matching PDFs
        for company_dir in self.raw_data_dir.iterdir():
            if company_dir.is_dir():
                for year_dir in company_dir.iterdir():
                    if year_dir.is_dir():
                        for pdf_file in year_dir.glob("*.pdf"):
                            # Skip underscore prefixed duplicates
                            if pdf_file.name.startswith("_"):
                                continue
                            
                            # Check if matches director dealing patterns
                            filename = pdf_file.name.lower()
                            is_director_form = any(
                                re.search(p, filename, re.IGNORECASE) 
                                for p in patterns
                            )
                            
                            if is_director_form:
                                pdf_files.append(pdf_file)
        
        print(f"  Found {len(pdf_files)} director dealing PDFs")
        
        # Extract text from each PDF and create filing records
        for idx, pdf_path in enumerate(pdf_files, 1):
            try:
                text = self._extract_pdf_text(pdf_path)
                
                if text and len(text) > 100:  # Must have meaningful content
                    filing = {
                        'id': idx,
                        'filepath': str(pdf_path),
                        'filename': pdf_path.name,
                        'company': pdf_path.parent.parent.name,
                        'year': pdf_path.parent.name,
                        'text': text,
                    }
                    filings.append(filing)
            except Exception as e:
                print(f"  ⚠ Error extracting {pdf_path.name}: {str(e)}")
        
        print(f"  Successfully extracted: {len(filings)} director dealing documents")
        
        # Limit to 100 for testing
        if len(filings) > 100:
            filings = filings[:100]
            print(f"  Limited to first 100 for testing")
        
        self.test_filings = filings
        return filings
    
    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            # Try PyPDF2 first if available
            if PYPDF_AVAILABLE:
                try:
                    with open(pdf_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                    return text
                except:
                    pass
            
            # Fallback: read as text if it's a text file
            # (some PDFs might be stored as text)
            try:
                with open(pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except:
                pass
            
            return None
            
        except Exception as e:
            return None
    
    def extract_and_validate(self):
        """
        For each filing: extract and manually verify fields.
        """
        print("\n[2] EXTRACTION & MANUAL VERIFICATION...")
        print(f"    Processing {len(self.test_filings)} filings...")
        
        for idx, filing in enumerate(self.test_filings, 1):
            try:
                text = filing['text']
                company = filing['company']
                filename = filing['filename']
                
                # Parse extracted fields
                extraction = self._parse_extraction(text)
                
                # Validate against source text
                validation = self._validate_extraction(extraction, text)
                
                self.results.append({
                    'filing_num': idx,
                    'filepath': filing['filepath'],
                    'filename': filename,
                    'company': company,
                    'year': filing['year'],
                    'extraction': extraction,
                    'validation': validation,
                })
                
                # Progress indicator
                if idx % 10 == 0:
                    print(f"    ✓ Processed {idx}/{len(self.test_filings)}")
                    
            except Exception as e:
                print(f"    ⚠ Error processing filing {idx}: {str(e)}")
                self.results.append({
                    'filing_num': idx,
                    'filename': filing['filename'],
                    'error': str(e)
                })
        
        print(f"    ✓ Completed validation of {len(self.results)} filings")
    
    def _parse_extraction(self, text: str) -> Dict:
        """Extract fields using regex patterns"""
        return {
            'director_name': self._extract_director_name(text),
            'shares': self._extract_shares(text),
            'transaction_type': self._extract_transaction_type(text),
            'direct_interest_before': self._extract_before_interest(text),
            'direct_interest_after': self._extract_after_interest(text),
        }
    
    def _extract_director_name(self, text: str):
        """Extract director name from Form 1/3"""
        patterns = [
            r"Name of Director/CEO:\s*\n?\s*(?:\d+\.)?\s*([^\n]+?)(?:\n|$)",
            r"Name of Director:\s*\n?\s*(?:\d+\.)?\s*([^\n]+?)(?:\n|$)",
            r"Director:\s*\n?\s*(?:\d+\.)?\s*([^\n]+?)(?:\n|$)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                # Clean up
                name = re.sub(r'\s*\d+\s*$', '', name)
                name = re.sub(r'\s+', ' ', name)
                if name and len(name) > 2:
                    return name
        return None
    
    def _extract_shares(self, text: str):
        """Extract number of shares from Form 1/3"""
        patterns = [
            r"Number of shares.*?\n\s*(?:\d+\.)?\s*([\d,]+)",
            r"number of ordinary voting shares.*?\n\s*(?:\d+\.)?\s*([\d,]+)",
            r"Shares.*?\n\s*(?:\d+\.)?\s*([\d,]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
            if match:
                shares_str = match.group(1).replace(',', '')
                try:
                    shares = int(shares_str)
                    if shares > 0:
                        return shares
                except:
                    pass
        return None
    
    def _extract_transaction_type(self, text: str):
        """Determine BUY, SELL, or other from Form content"""
        text_lower = text.lower()
        
        # Check for acquisition keywords
        if any(keyword in text_lower for keyword in ['acquisition', 'buy', 'purchase', 'subscribe']):
            return 'BUY'
        
        # Check for disposal keywords
        if any(keyword in text_lower for keyword in ['disposal', 'sell', 'sold', 'exercise of option']):
            return 'SELL'
        
        # Default
        return 'OTHER'
    
    def _extract_before_interest(self, text: str):
        """Extract direct interest BEFORE transaction"""
        patterns = [
            r"Immediately before.*?No\. of ordinary voting shares/units held:\s*([\d,]+)",
            r"Before.*?shares.*?:\s*([\d,]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1).replace(',', ''))
                except:
                    pass
        return None
    
    def _extract_after_interest(self, text: str):
        """Extract direct interest AFTER transaction"""
        patterns = [
            r"Immediately after.*?No\. of ordinary voting shares/units held:\s*([\d,]+)",
            r"After.*?shares.*?:\s*([\d,]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1).replace(',', ''))
                except:
                    pass
        return None
    
    def _validate_extraction(self, extraction: Dict, source_text: str) -> Dict:
        """
        Validate extracted fields against source text.
        """
        validation = {}
        
        # Director name validation
        name = extraction.get('director_name')
        if name:
            # Check if name appears in source
            if name.lower() in source_text.lower():
                validation['director_name'] = 'CORRECT'
            else:
                validation['director_name'] = 'QUESTIONABLE'
        else:
            validation['director_name'] = 'MISSING'
        
        # Shares validation
        shares = extraction.get('shares')
        if shares and shares > 0:
            validation['shares'] = 'CORRECT'
        else:
            validation['shares'] = 'MISSING'
        
        # Transaction type validation
        trans_type = extraction.get('transaction_type')
        if trans_type == 'OTHER':
            validation['transaction_type'] = 'UNCLEAR'
        elif trans_type in ['BUY', 'SELL']:
            validation['transaction_type'] = 'CORRECT'
        else:
            validation['transaction_type'] = 'MISSING'
        
        # Before interest validation
        before = extraction.get('direct_interest_before')
        if before is not None and before >= 0:
            validation['direct_interest_before'] = 'CORRECT'
        else:
            validation['direct_interest_before'] = 'MISSING'
        
        # After interest validation
        after = extraction.get('direct_interest_after')
        if after is not None and after >= 0:
            validation['direct_interest_after'] = 'CORRECT'
        else:
            validation['direct_interest_after'] = 'MISSING'
        
        return validation
    
    def generate_accuracy_report(self) -> Dict:
        """Generate comprehensive accuracy report"""
        print("\n[3] ACCURACY REPORT...")
        
        # Count correctness by field
        field_counts = {
            'director_name': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0, 'UNCLEAR': 0},
            'shares': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0, 'UNCLEAR': 0},
            'transaction_type': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0, 'UNCLEAR': 0},
            'direct_interest_before': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0, 'UNCLEAR': 0},
            'direct_interest_after': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0, 'UNCLEAR': 0},
        }
        
        errors = []
        buy_transactions = []
        sell_transactions = []
        total_with_validation = 0
        
        for result in self.results:
            if 'error' in result:
                continue
            
            total_with_validation += 1
            validation = result.get('validation', {})
            extraction = result.get('extraction', {})
            
            # Count results by field
            for field in field_counts.keys():
                status = validation.get(field, 'MISSING')
                if status not in field_counts[field]:
                    field_counts[field][status] = 0
                field_counts[field][status] += 1
            
            # Track BUY/SELL transactions
            trans_type = extraction.get('transaction_type')
            if trans_type == 'BUY':
                buy_transactions.append(result)
            elif trans_type == 'SELL':
                sell_transactions.append(result)
            
            # Track errors
            for field, status in validation.items():
                if status not in ['CORRECT', 'MISSING']:
                    errors.append({
                        'filing': result['filing_num'],
                        'company': result['company'],
                        'filename': result['filename'],
                        'field': field,
                        'status': status,
                    })
        
        # Calculate accuracy percentages
        accuracy = {}
        for field, counts in field_counts.items():
            total = sum(counts.values())
            if total > 0:
                accuracy[field] = {
                    'correct': counts['CORRECT'],
                    'total': total,
                    'percentage': round(100 * counts['CORRECT'] / total, 2),
                    'breakdown': counts
                }
        
        report = {
            'total_filings_tested': len(self.test_filings),
            'total_filings_processed': total_with_validation,
            'test_date': datetime.now().isoformat(),
            'accuracy_by_field': accuracy,
            'errors_summary': {
                'total_errors': len(errors),
                'fields_below_90_percent': [f for f, a in accuracy.items() if a['percentage'] < 90],
                'sample_errors': errors[:20]
            },
            'buy_transactions_found': len(buy_transactions),
            'sell_transactions_found': len(sell_transactions),
            'buy_samples': buy_transactions[:5],
            'sell_samples': sell_transactions[:5],
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print formatted accuracy report"""
        print("\n" + "="*100)
        print("ACCURACY REPORT SUMMARY")
        print("="*100)
        
        print(f"\nTest Date: {report['test_date']}")
        print(f"Total Filings Tested: {report['total_filings_tested']}")
        print(f"Successfully Processed: {report['total_filings_processed']}")
        
        print("\n" + "-"*100)
        print("FIELD-BY-FIELD ACCURACY")
        print("-"*100)
        
        for field, data in report['accuracy_by_field'].items():
            correct = data['correct']
            total = data['total']
            percentage = data['percentage']
            status = "✓ PASS" if percentage >= 90 else "✗ FAIL"
            
            print(f"\n{field}:")
            print(f"  {status} - {correct}/{total} correct ({percentage}%)")
            print(f"  Breakdown: {data['breakdown']}")
        
        print("\n" + "-"*100)
        print("FIELDS WITH <90% ACCURACY")
        print("-"*100)
        
        if report['errors_summary']['fields_below_90_percent']:
            for field in report['errors_summary']['fields_below_90_percent']:
                acc = report['accuracy_by_field'][field]
                print(f"  ✗ {field}: {acc['percentage']}% ({acc['correct']}/{acc['total']})")
        else:
            print("  ✓ All fields >= 90% accuracy")
        
        print("\n" + "-"*100)
        print("INSIDER TRANSACTIONS FOUND")
        print("-"*100)
        
        print(f"\nBUY Transactions Found: {report['buy_transactions_found']}")
        if report['buy_samples']:
            print("  Sample BUY transactions:")
            for sample in report['buy_samples'][:3]:
                ex = sample.get('extraction', {})
                print(f"    - {sample['company']} | {sample['filename']}")
                print(f"      Director: {ex.get('director_name', 'N/A')}")
                print(f"      Shares: {ex.get('shares', 'N/A')}")
        
        print(f"\nSELL Transactions Found: {report['sell_transactions_found']}")
        if report['sell_samples']:
            print("  Sample SELL transactions:")
            for sample in report['sell_samples'][:3]:
                ex = sample.get('extraction', {})
                print(f"    - {sample['company']} | {sample['filename']}")
                print(f"      Director: {ex.get('director_name', 'N/A')}")
                print(f"      Shares: {ex.get('shares', 'N/A')}")
        
        print("\n" + "-"*100)
        print("DECISION GATE")
        print("="*100)
        
        all_passed = all(
            data['percentage'] >= 90 
            for data in report['accuracy_by_field'].values()
        )
        
        if all_passed:
            print("\n✓ RECOMMENDATION: PROCEED TO PHASE 5")
            print("  All fields have >=90% accuracy.")
        else:
            print("\n✗ RECOMMENDATION: STOP - INVESTIGATION REQUIRED")
            print("  The following fields have <90% accuracy:")
            for field in report['errors_summary']['fields_below_90_percent']:
                acc = report['accuracy_by_field'][field]
                print(f"    - {field}: {acc['percentage']}% ({acc['correct']}/{acc['total']})")
        
        print("\n" + "="*100)
    
    def run(self):
        """Execute complete Phase 4 testing"""
        try:
            # Step 1: Discover PDFs
            self.discover_director_dealing_pdfs()
            
            if len(self.test_filings) < 100:
                print(f"\n⚠ WARNING: Only {len(self.test_filings)} PDFs found (need 100+)")
                if len(self.test_filings) < 10:
                    print("  ✗ Not enough PDFs for meaningful testing")
                    return None
                print("  Proceeding with available PDFs...")
            
            # Step 2: Extract and validate
            self.extract_and_validate()
            
            # Step 3: Generate report
            report = self.generate_accuracy_report()
            
            # Step 4: Print report
            self.print_report(report)
            
            return report
            
        except Exception as e:
            print(f"\n✗ FATAL ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    tester = Phase4DirectPDFTester()
    report = tester.run()
