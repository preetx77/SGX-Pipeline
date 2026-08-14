"""
Form 1 Transaction Type Extraction Test

Tests extraction of transaction types from all Form 1 PDFs.
Prints actual extraction results for inspection.
"""

import fitz
import glob
from classifiers.director_dealings_classifier import DirectorDealingsClassifier
from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor

extractor = DirectorDealingsExtractor()
classifier = DirectorDealingsClassifier()

# Find all Form 1 files
form1_files = sorted([
    f for f in glob.glob('data/raw/**/*.pdf', recursive=True)
    if ('form 1' in f.lower() or 'form1' in f.lower() or 'eform1' in f.lower())
    and 'orm' in f.lower()
])

# Filter to text-extractable only
extractable_form1s = []
for f in form1_files:
    try:
        doc = fitz.open(f)
        text = ''.join(p.get_text() for p in doc)
        if len(text.strip()) > 2000:
            extractable_form1s.append((f, text))
    except:
        pass

print("="*80)
print("FORM 1 TRANSACTION TYPE EXTRACTION TEST")
print("="*80)
print(f"\nFound {len(extractable_form1s)} text-extractable Form 1 files\n")

results = []

for filepath, text in extractable_form1s:
    filename = filepath.split('\\')[-1]
    
    # Extract all fields
    director = extractor.extract_director(text)
    shares = extractor.extract_shares(text)
    price = extractor.extract_price(text)
    before = extractor.extract_direct_interest_before(text)
    after = extractor.extract_direct_interest_after(text)
    transaction_type = classifier.classify(text)
    
    results.append({
        'filename': filename,
        'director': director,
        'transaction_type': transaction_type,
        'shares': shares,
        'price': price,
        'before': before,
        'after': after
    })
    
    # Print individual results
    print("="*80)
    print(f"FILE: {filename}")
    print("="*80)
    print(f"Director: {director or '[NO NAME]'}")
    print(f"Transaction: {transaction_type}")
    print(f"Shares: {shares}")
    print(f"Price: {price}")
    print(f"Before: {before}")
    print(f"After: {after}")
    print()

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

transaction_counts = {}
for r in results:
    tx_type = r['transaction_type']
    transaction_counts[tx_type] = transaction_counts.get(tx_type, 0) + 1

print(f"\nForm 1 transaction extraction  Tested: {len(results)}")
for tx_type in sorted(transaction_counts.keys()):
    count = transaction_counts[tx_type]
    print(f"  {tx_type:20} {count:2}")

unknown_count = transaction_counts.get('UNKNOWN', 0)
if unknown_count > 0:
    print(f"\n⚠ {unknown_count} transactions remain UNKNOWN — need to inspect PDFs")

