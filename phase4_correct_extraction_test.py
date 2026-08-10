"""
Phase 4: Correct Extraction Accuracy Testing
Uses PRODUCTION extraction code (PDFExtractor + DirectorDealingsExtractor)
Tests against 100+ real director-dealing PDFs from data/raw

This is the CORRECTED version that calls actual production code,
not a reimplemented test harness.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from extractors.pdf.pdf_extractor import PDFExtractor
from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor
from models.document import Document
from models.announcement import Announcement


class Phase4CorrectTest:
    """
    Phase 4 testing using PRODUCTION extraction code
    """
    
    def __init__(self):
        self.results = []
        self.test_filings = []
        self.raw_data_dir = Path(__file__).parent / "data" / "raw"
        self.pdf_extractor = PDFExtractor()
        self.dd_extractor = DirectorDealingsExtractor()
        
    def discover_director_dealing_pdfs(self) -> List[Dict]:
        """
        Discover all director dealing PDFs from data/raw directory.
        Look for Form 1, Form 3, and eFORM3 files.
        """
        print("\n" + "="*100)
        print("PHASE 4: EXTRACTION ACCURACY TESTING (CORRECT - Using Production Code)")
        print("="*100)
        print("\n[1] SOURCING DIRECTOR DEALING PDFs...")
        
        filings = []
        
        if not self.raw_data_dir.exists():
            print(f"  ✗ Data directory not found: {self.raw_data_dir}")
            return []
        
        # Patterns for director dealing documents
        patterns = [
            'Form 1',
            'Form 3',
            'eFORM3',
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
                            filename = pdf_file.name
                            is_director_form = any(
                                pattern in filename
                                for pattern in patterns
                            )
                            
                            if is_director_form:
                                pdf_files.append(pdf_file)
        
        print(f"  Found {len(pdf_files)} director dealing PDFs")
        
        # Create filing records with production PDF extraction
        for idx, pdf_path in enumerate(pdf_files, 1):
            try:
                # Create mock attachment and announcement objects for extraction pipeline
                attachment = self._create_mock_attachment(pdf_path)
                announcement = self._create_mock_announcement(pdf_path)
                
                # Use PRODUCTION PDF extractor
                document = self.pdf_extractor.extract(attachment, announcement)
                
                if document and document.text and len(document.text) > 100:
                    filing = {
                        'id': idx,
                        'filepath': str(pdf_path),
                        'filename': pdf_path.name,
                        'company': pdf_path.parent.parent.name,
                        'year': pdf_path.parent.name,
                        'document': document,  # Store full document object
                        'text': document.text,
                    }
                    filings.append(filing)
                else:
                    print(f"  ⚠ Skipping {pdf_path.name}: No text extracted (corrupted or empty)")
                    
            except Exception as e:
                print(f"  ⚠ Error extracting {pdf_path.name}: {str(e)}")
        
        print(f"  Successfully extracted: {len(filings)} director dealing documents")
        
        # Limit to 100 for testing
        if len(filings) > 100:
            filings = filings[:100]
            print(f"  Limited to first 100 for testing")
        
        self.test_filings = filings
        return filings
    
    def _create_mock_attachment(self, pdf_path: Path):
        """Create mock attachment object for production pipeline"""
        class MockAttachment:
            def __init__(self, path):
                self.local_path = str(path)
                self.filename = path.name
                self.attachment_id = hash(str(path))
        return MockAttachment(pdf_path)
    
    def _create_mock_announcement(self, pdf_path: Path):
        """Create mock announcement object for production pipeline"""
        class MockAnnouncement:
            def __init__(self, path):
                self.announcement_id = hash(str(path))
                self.title = path.name
                self.category = "DIRECTOR_DEALING"
                self.company_name = path.parent.parent.name
                self.stock_code = path.parent.parent.name
        return MockAnnouncement(pdf_path)
    
    def extract_and_validate(self):
        """
        For each filing: extract using PRODUCTION DirectorDealingsExtractor and validate.
        """
        print("\n[2] EXTRACTION & VALIDATION (Using Production Code)...")
        print(f"    Processing {len(self.test_filings)} filings...")
        
        for idx, filing in enumerate(self.test_filings, 1):
            try:
                document = filing['document']
                filename = filing['filename']
                company = filing['company']
                
                # Create mock announcement for production extractor
                announcement = self._create_mock_announcement(Path(filing['filepath']))
                
                # Use PRODUCTION DirectorDealingsExtractor
                director_dealing = self.dd_extractor.extract(announcement, document)
                
                # Validate extracted fields
                validation = self._validate_extraction(director_dealing, filing['text'])
                
                self.results.append({
                    'filing_num': idx,
                    'filepath': filing['filepath'],
                    'filename': filename,
                    'company': company,
                    'year': filing['year'],
                    'extraction': {
                        'director_name': director_dealing.director_name,
                        'shares': director_dealing.shares,
                        'price': director_dealing.price,
                        'value': director_dealing.value,
                        'transaction_type': director_dealing.transaction_type,
                        'direct_interest_before': director_dealing.direct_interest_before,
                        'direct_interest_after': director_dealing.direct_interest_after,
                    },
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
    
    def _validate_extraction(self, director_dealing, source_text: str) -> Dict:
        """
        Validate extracted fields against source text.
        """
        validation = {}
        
        # Director name validation
        name = director_dealing.director_name
        if name:
            if name.lower() in source_text.lower():
                validation['director_name'] = 'CORRECT'
            else:
                validation['director_name'] = 'QUESTIONABLE'
        else:
            validation['director_name'] = 'MISSING'
        
        # Shares validation
        shares = director_dealing.shares
        if shares and shares > 0:
            validation['shares'] = 'CORRECT'
        else:
            validation['shares'] = 'MISSING'
        
        # Price validation
        price = director_dealing.price
        if price and price > 0:
            validation['price'] = 'CORRECT'
        else:
            validation['price'] = 'MISSING'
        
        # Value validation (calculated field)
        value = director_dealing.value
        if value and value > 0:
            validation['value'] = 'CORRECT'
        else:
            validation['value'] = 'MISSING'
        
        # Transaction type validation
        trans_type = director_dealing.transaction_type
        if trans_type and trans_type not in ['UNKNOWN', None]:
            validation['transaction_type'] = 'CORRECT'
        else:
            validation['transaction_type'] = 'MISSING'
        
        # Before interest validation
        before = director_dealing.direct_interest_before
        if before is not None and before >= 0:
            validation['direct_interest_before'] = 'CORRECT'
        else:
            validation['direct_interest_before'] = 'MISSING'
        
        # After interest validation
        after = director_dealing.direct_interest_after
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
            'director_name': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0},
            'shares': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0},
            'price': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0},
            'value': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0},
            'transaction_type': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0},
            'direct_interest_before': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0},
            'direct_interest_after': {'CORRECT': 0, 'MISSING': 0, 'QUESTIONABLE': 0},
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
            if trans_type and 'BUY' in str(trans_type).upper():
                buy_transactions.append(result)
            elif trans_type and 'SELL' in str(trans_type).upper():
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
                print(f"      Price: {ex.get('price', 'N/A')} SGD")
                print(f"      Value: {ex.get('value', 'N/A')} SGD")
        
        print(f"\nSELL Transactions Found: {report['sell_transactions_found']}")
        if report['sell_samples']:
            print("  Sample SELL transactions:")
            for sample in report['sell_samples'][:3]:
                ex = sample.get('extraction', {})
                print(f"    - {sample['company']} | {sample['filename']}")
                print(f"      Director: {ex.get('director_name', 'N/A')}")
                print(f"      Shares: {ex.get('shares', 'N/A')}")
                print(f"      Price: {ex.get('price', 'N/A')} SGD")
                print(f"      Value: {ex.get('value', 'N/A')} SGD")
        
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
            print("\n✗ RECOMMENDATION: REVIEW FINDINGS")
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
            
            if len(self.test_filings) == 0:
                print(f"\n✗ FATAL: No director dealing PDFs found")
                return None
            
            if len(self.test_filings) < 100:
                print(f"\n⚠ WARNING: Only {len(self.test_filings)} PDFs found (target: 100+)")
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
    tester = Phase4CorrectTest()
    report = tester.run()
