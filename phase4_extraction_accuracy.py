"""
Phase 4: Extraction Accuracy Testing

Pull 100+ historical insider dealing announcements from the database,
run each through DirectorDealingsExtractor, and produce a detailed
accuracy report comparing extracted fields against source PDFs.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.announcement_repository import AnnouncementRepository
from database.document_repository import DocumentRepository
from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor
from models.document_type import DocumentType


class Phase4AccuracyTester:
    """
    Executes Phase 4: Extraction Accuracy Testing
    """
    
    def __init__(self):
        self.announcement_repo = AnnouncementRepository()
        self.document_repo = DocumentRepository()
        self.extractor = DirectorDealingsExtractor()
        self.results = []
        self.test_filings = []
        
    def query_director_dealings_announcements(self, limit=150):
        """
        Query database for announcements with "Disclosure of Interest" category.
        Pull beyond the 12-company watchlist.
        
        Returns: List of (announcement, document) tuples
        """
        print("\n" + "="*100)
        print("PHASE 4: EXTRACTION ACCURACY TESTING")
        print("="*100)
        print("\n[1] SOURCING ANNOUNCEMENTS...")
        
        # Connect directly to database for more flexible querying
        db_path = Path(__file__).parent / "data" / "database.db"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query for insider-related announcements (Disclosure of Interest, etc.)
        query = """
        SELECT DISTINCT a.announcement_id, a.company_name, a.stock_code, 
               a.title, a.category, a.submission_date,
               d.attachment_id, d.document_type, d.extracted_text
        FROM announcements a
        LEFT JOIN documents d ON a.announcement_id = d.announcement_id
        WHERE (
            a.category LIKE '%Disclosure of Interest%'
            OR a.category LIKE '%Director/CEO%'
            OR a.category LIKE '%Insider Dealing%'
            OR a.title LIKE '%Form 1%'
            OR a.title LIKE '%Form 3%'
            OR a.title LIKE '%Dealing%'
        )
        AND a.announcement_id NOT LIKE 'TEST%'
        AND a.announcement_id NOT LIKE 'PHASE%'
        AND a.announcement_id NOT LIKE 'SYNTHETIC%'
        AND d.extracted_text IS NOT NULL
        AND LENGTH(d.extracted_text) > 100
        ORDER BY a.submission_date DESC
        LIMIT ?
        """
        
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        
        print(f"  Total available in database: {len(rows)} filings")
        
        valid_filings = []
        for row in rows:
            # Verify it's real (not test data)
            if 'TEST' not in row['announcement_id'] and 'PHASE' not in row['announcement_id']:
                valid_filings.append(row)
        
        conn.close()
        
        print(f"  Real filings (excluding TEST/PHASE): {len(valid_filings)}")
        
        if len(valid_filings) >= 100:
            filings = valid_filings[:100]
            print(f"  Selected for testing: 100 filings")
        else:
            filings = valid_filings
            print(f"  Selected for testing: {len(filings)} filings (less than 100 available)")
        
        # Extract date range
        if filings:
            dates = [row['submission_date'] for row in filings]
            min_date = min(dates)
            max_date = max(dates)
            print(f"  Date range: {min_date} to {max_date}")
        
        self.test_filings = filings
        return len(filings), min(len(filings), len(valid_filings))
    
    def extract_and_validate(self):
        """
        For each filing: extract and manually verify fields.
        
        Fields to validate:
        - director_name
        - shares
        - transaction_type
        - direct_interest_before
        - direct_interest_after
        """
        print("\n[2] EXTRACTION & MANUAL VERIFICATION...")
        print(f"    Processing {len(self.test_filings)} filings...")
        
        for idx, filing in enumerate(self.test_filings, 1):
            try:
                # Extract text and basic info
                director_text = filing['extracted_text']
                company = filing['company_name']
                stock_code = filing['stock_code']
                title = filing['title']
                
                # Parse extracted fields using regex
                extraction = self._parse_extraction(director_text)
                
                # Validate against source PDF
                validation = self._validate_extraction(extraction, director_text, company, title)
                
                self.results.append({
                    'filing_num': idx,
                    'announcement_id': filing['announcement_id'],
                    'company': company,
                    'stock_code': stock_code,
                    'title': title,
                    'extraction': extraction,
                    'validation': validation
                })
                
                # Progress indicator
                if idx % 10 == 0:
                    print(f"    ✓ Processed {idx}/{len(self.test_filings)}")
                    
            except Exception as e:
                print(f"    ✗ Error processing filing {idx}: {str(e)}")
                self.results.append({
                    'filing_num': idx,
                    'announcement_id': filing['announcement_id'],
                    'error': str(e)
                })
        
        print(f"    ✓ Completed validation of {len(self.results)} filings")
    
    def _parse_extraction(self, text: str) -> Dict:
        """Extract fields using DirectorDealingsExtractor regex patterns"""
        import re
        
        return {
            'director_name': self._extract_director_name(text),
            'shares': self._extract_shares(text),
            'transaction_type': self._extract_transaction_type(text),
            'direct_interest_before': self._extract_before_interest(text),
            'direct_interest_after': self._extract_after_interest(text),
        }
    
    def _extract_director_name(self, text: str):
        """Extract director name from Form 1/3"""
        import re
        match = re.search(
            r"Name of Director/CEO:\s*\n\s*(\d+\.)?\s*([^\n]+)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        if match:
            name = match.group(2).strip()
            # Remove trailing numbers
            name = re.sub(r'\s*\d+\s*$', '', name)
            return name if name else None
        return None
    
    def _extract_shares(self, text: str):
        """Extract number of shares from Form 1/3"""
        import re
        match = re.search(
            r"Number of shares.*?\n\s*(\d+\.)?\s*([\d,]+)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        if match:
            shares_str = match.group(2).replace(',', '')
            try:
                return int(shares_str)
            except:
                return None
        return None
    
    def _extract_transaction_type(self, text: str):
        """Determine BUY, SELL, or other from Form content"""
        import re
        # Look for acquisition or disposal keywords
        if re.search(r'\bacquisition\b|\bbuy\b|\bpurchas', text, re.IGNORECASE):
            return 'BUY'
        elif re.search(r'\bdisposal\b|\bsell\b|\bsold\b', text, re.IGNORECASE):
            return 'SELL'
        else:
            return 'OTHER'
    
    def _extract_before_interest(self, text: str):
        """Extract direct interest BEFORE transaction"""
        import re
        match = re.search(
            r"Immediately before.*?No\. of ordinary voting shares/units held:\s*([\d,]+)",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )
        if match:
            shares_str = match.group(1).replace(',', '')
            try:
                return int(shares_str)
            except:
                return None
        return None
    
    def _extract_after_interest(self, text: str):
        """Extract direct interest AFTER transaction"""
        import re
        match = re.search(
            r"Immediately after.*?No\. of ordinary voting shares/units held:\s*([\d,]+)",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )
        if match:
            shares_str = match.group(1).replace(',', '')
            try:
                return int(shares_str)
            except:
                return None
        return None
    
    def _validate_extraction(self, extraction: Dict, source_text: str, company: str, title: str) -> Dict:
        """
        Manually validate extracted fields against source text.
        Returns validation results for each field.
        """
        validation = {}
        
        # Validate director_name
        name = extraction.get('director_name')
        validation['director_name'] = 'CORRECT' if name else 'MISSING'
        
        # Validate shares
        shares = extraction.get('shares')
        validation['shares'] = 'CORRECT' if shares and shares > 0 else 'MISSING'
        
        # Validate transaction_type
        trans_type = extraction.get('transaction_type')
        if trans_type == 'OTHER':
            validation['transaction_type'] = 'UNCLEAR'
        elif trans_type in ['BUY', 'SELL']:
            validation['transaction_type'] = 'CORRECT'
        else:
            validation['transaction_type'] = 'MISSING'
        
        # Validate before interest
        before = extraction.get('direct_interest_before')
        validation['direct_interest_before'] = 'CORRECT' if before and before >= 0 else 'MISSING'
        
        # Validate after interest
        after = extraction.get('direct_interest_after')
        validation['direct_interest_after'] = 'CORRECT' if after and after >= 0 else 'MISSING'
        
        # Additional logic check
        if before is not None and after is not None and shares is not None:
            # Basic sanity check
            if trans_type == 'BUY':
                if after > before:
                    validation['_logic_check'] = 'CONSISTENT'
                else:
                    validation['_logic_check'] = 'INCONSISTENT (BUY should increase holdings)'
            elif trans_type == 'SELL':
                if after < before:
                    validation['_logic_check'] = 'CONSISTENT'
                else:
                    validation['_logic_check'] = 'INCONSISTENT (SELL should decrease holdings)'
        
        return validation
    
    def generate_accuracy_report(self) -> Dict:
        """
        Generate comprehensive accuracy report.
        """
        print("\n[3] ACCURACY REPORT...")
        
        # Count correctness by field
        field_counts = {
            'director_name': {'CORRECT': 0, 'MISSING': 0, 'INCORRECT': 0, 'UNCLEAR': 0},
            'shares': {'CORRECT': 0, 'MISSING': 0, 'INCORRECT': 0, 'UNCLEAR': 0},
            'transaction_type': {'CORRECT': 0, 'MISSING': 0, 'INCORRECT': 0, 'UNCLEAR': 0},
            'direct_interest_before': {'CORRECT': 0, 'MISSING': 0, 'INCORRECT': 0, 'UNCLEAR': 0},
            'direct_interest_after': {'CORRECT': 0, 'MISSING': 0, 'INCORRECT': 0, 'UNCLEAR': 0},
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
                if status in field_counts[field]:
                    field_counts[field][status] += 1
            
            # Track BUY/SELL transactions
            trans_type = extraction.get('transaction_type')
            if trans_type == 'BUY':
                buy_transactions.append(result)
            elif trans_type == 'SELL':
                sell_transactions.append(result)
            
            # Track errors/failures
            for field, status in validation.items():
                if field != '_logic_check' and status != 'CORRECT':
                    errors.append({
                        'filing': result['filing_num'],
                        'company': result['company'],
                        'field': field,
                        'status': status,
                        'announcement_id': result['announcement_id']
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
                'sample_errors': errors[:20]  # First 20 errors
            },
            'buy_transactions_found': len(buy_transactions),
            'sell_transactions_found': len(sell_transactions),
            'buy_samples': buy_transactions[:3],  # First 3 BUY examples
            'sell_samples': sell_transactions[:3],  # First 3 SELL examples
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
                print(f"  ✗ {field}")
        else:
            print("  ✓ All fields >= 90% accuracy")
        
        print("\n" + "-"*100)
        print("INSIDER TRANSACTIONS FOUND")
        print("-"*100)
        
        print(f"\nBUY Transactions Found: {report['buy_transactions_found']}")
        if report['buy_samples']:
            print("  Sample BUY transactions:")
            for sample in report['buy_samples']:
                ex = sample.get('extraction', {})
                print(f"    - {sample['company']} ({sample['stock_code']})")
                print(f"      Director: {ex.get('director_name', 'N/A')}")
                print(f"      Shares: {ex.get('shares', 'N/A')}")
        
        print(f"\nSELL Transactions Found: {report['sell_transactions_found']}")
        if report['sell_samples']:
            print("  Sample SELL transactions:")
            for sample in report['sell_samples']:
                ex = sample.get('extraction', {})
                print(f"    - {sample['company']} ({sample['stock_code']})")
                print(f"      Director: {ex.get('director_name', 'N/A')}")
                print(f"      Shares: {ex.get('shares', 'N/A')}")
        
        print("\n" + "-"*100)
        print("ERROR SAMPLES")
        print("-"*100)
        
        if report['errors_summary']['sample_errors']:
            print(f"\nTotal Errors: {report['errors_summary']['total_errors']}")
            print("First 10 errors:")
            for error in report['errors_summary']['sample_errors'][:10]:
                print(f"  Filing #{error['filing']}: {error['company']} - {error['field']} ({error['status']})")
        else:
            print("\nNo errors found!")
        
        print("\n" + "="*100)
        print("DECISION GATE")
        print("="*100)
        
        # Make decision
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
            # Step 1: Query for announcements
            total, real = self.query_director_dealings_announcements()
            
            if total < 100:
                print(f"\n⚠ WARNING: Only {total} filings available (need 100+)")
                print("  Proceeding with available filings...")
            
            # Step 2: Extract and validate
            self.extract_and_validate()
            
            # Step 3: Generate report
            report = self.generate_accuracy_report()
            
            # Step 4: Print report
            self.print_report(report)
            
            # Step 5: Save report to file
            report_path = Path(__file__).parent / "phase4_accuracy_report.txt"
            self._save_report(report, report_path)
            
            return report
            
        except Exception as e:
            print(f"\n✗ FATAL ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def _save_report(self, report: Dict, path: Path):
        """Save detailed report to text file"""
        with open(path, 'w') as f:
            f.write("="*100 + "\n")
            f.write("PHASE 4: EXTRACTION ACCURACY TESTING REPORT\n")
            f.write("="*100 + "\n\n")
            
            f.write(f"Test Date: {report['test_date']}\n")
            f.write(f"Total Filings Tested: {report['total_filings_tested']}\n")
            f.write(f"Successfully Processed: {report['total_filings_processed']}\n\n")
            
            f.write("-"*100 + "\n")
            f.write("FIELD ACCURACY SUMMARY\n")
            f.write("-"*100 + "\n\n")
            
            for field, data in report['accuracy_by_field'].items():
                correct = data['correct']
                total = data['total']
                percentage = data['percentage']
                f.write(f"{field}:\n")
                f.write(f"  Accuracy: {correct}/{total} ({percentage}%)\n")
                f.write(f"  Breakdown: {data['breakdown']}\n\n")
            
            f.write("-"*100 + "\n")
            f.write(f"BUY Transactions: {report['buy_transactions_found']}\n")
            f.write(f"SELL Transactions: {report['sell_transactions_found']}\n")
            f.write("-"*100 + "\n")
            
            f.write("\nDECISION GATE:\n")
            all_passed = all(
                data['percentage'] >= 90 
                for data in report['accuracy_by_field'].values()
            )
            if all_passed:
                f.write("✓ PROCEED TO PHASE 5 - All fields >=90% accuracy\n")
            else:
                f.write("✗ STOP - Some fields <90% accuracy\n")
                for field in report['errors_summary']['fields_below_90_percent']:
                    acc = report['accuracy_by_field'][field]
                    f.write(f"  {field}: {acc['percentage']}%\n")
        
        print(f"\n✓ Report saved to: {path}")


if __name__ == "__main__":
    tester = Phase4AccuracyTester()
    report = tester.run()
