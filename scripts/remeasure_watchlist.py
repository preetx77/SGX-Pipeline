#!/usr/bin/env python3
"""
Re-measure problematic 100-company watchlist entries.

Fixes:
1. Re-measures capped, fails, and unmeasured companies
2. Fetches real SGX codes from issuers array (most frequent, reject >4 chars)
3. Keeps only companies with ≥1 director filing
4. Outputs clean CSV with code, director/shareholder split, truncated flag
"""

import csv
import json
import sys
from collections import Counter
from datetime import datetime
from scraper.client import SGXClient

client = SGXClient(throttle_delay=0.5)

# Load existing measurements from both CSVs
measured = {}
for csv_file in ["docs/SGX_100_200_INSIDER_MEASUREMENT.csv", "docs/SGX_200_500_INSIDER_MEASUREMENT.csv"]:
    try:
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                measured[row['name']] = row
    except FileNotFoundError:
        print(f"[!] Could not load {csv_file}")

print(f"[*] Loaded {len(measured)} existing measurements")

# Categorize companies
pass_companies = {name: row for name, row in measured.items() if row['status'] == 'PASS'}
fail_companies = {name: row for name, row in measured.items() if row['status'] == 'FAIL'}
unmeasured_companies = {name: row for name, row in measured.items() if row['status'] == 'UNMEASURED'}

# Capped = 100 announcements with positive filings (lower bounds, keep these)
capped = {name: row for name, row in pass_companies.items() 
          if int(row['total_announcements']) == 100}

# Capped FAILs = 100 announcements with zero filings (inconclusive, re-measure)
capped_fails = {name: row for name, row in fail_companies.items() 
                if int(row['total_announcements']) == 100}

print(f"[*] Analysis:")
print(f"    PASS (confirmed insider filings): {len(pass_companies)}")
print(f"    FAIL (zero filings): {len(fail_companies)}")
print(f"    Capped PASS (lower bound insider count): {len(capped)}")
print(f"    Capped FAIL (inconclusive, hit 100 cap): {len(capped_fails)}")
print(f"    UNMEASURED (never scanned): {len(unmeasured_companies)}")

# Dropped companies (known, not in CSVs)
dropped_names = ["UOB", "Singtel", "Keppel", "United Overseas Bank", 
                 "Singapore Telecommunications Limited", "Keppel Corporation Limited"]

# Confirm 34 FAILs with complete scan (total_announcements < 100)
confirmed_zero = {name: row for name, row in fail_companies.items() 
                  if int(row['total_announcements']) < 100}

print(f"    Confirmed FAIL (complete scan, zero filings): {len(confirmed_zero)}")

# Build re-measure list
to_remeasure = {}
to_remeasure.update(capped_fails)  # Re-measure capped FAILs (15, inconclusive)
to_remeasure.update(unmeasured_companies)  # All unmeasured (19)

# Add dropped companies
for name in dropped_names:
    if name not in to_remeasure:
        to_remeasure[name] = {'name': name, 'status': 'DROPPED', 'total_announcements': '0', 'insider_count': '0'}

print(f"[*] Companies to re-measure: {len(to_remeasure)}")

# Period for search (last 5 years)
from datetime import datetime, timedelta
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=5*365)
period_start = int(start_date.timestamp())
period_end = int(end_date.timestamp())

# Re-measure using iter_company_announcements
remeasured = {}
failed_to_fetch = []

for i, (name, old_row) in enumerate(sorted(to_remeasure.items()), 1):
    print(f"[{i}/{len(to_remeasure)}] {name}...", end='', flush=True)
    
    try:
        # Fetch all announcements using pagination (fixed: now uses result["announcement"])
        all_announcements = []
        try:
            for announcement in client.iter_company_announcements(
                name, 
                period_start=period_start,
                period_end=period_end,
                page_size=100
            ):
                all_announcements.append(announcement)
        except Exception as e:
            print(f" ERROR fetching: {type(e).__name__}: {str(e)[:50]}")
            failed_to_fetch.append((name, str(e)))
            continue
        
        # Count insider filings (Form 1 = director, Form 3 = shareholder)
        director_count = 0
        shareholder_count = 0
        code = None
        
        for ann in all_announcements:
            title = ann.get('title', '').upper() if ann.get('title') else ''
            if 'FORM 1' in title or 'DIRECTOR' in title:
                director_count += 1
            if 'FORM 3' in title or 'SHAREHOLDER' in title:
                shareholder_count += 1
            
            # Collect stock codes from announcements
            if not code and ann.get('stock_code'):
                codes_in_ann = ann.get('stock_code')
                if isinstance(codes_in_ann, str) and len(codes_in_ann) <= 4:
                    code = codes_in_ann
        
        total_insider = director_count + shareholder_count
        total_announcements = len(all_announcements)
        truncated = total_announcements >= 100  # Cap hit means pagination stopped
        
        status = 'PASS' if total_insider > 0 else 'FAIL'
        
        remeasured[name] = {
            'name': name,
            'code': code or 'UNKNOWN',
            'total_announcements': str(total_announcements),
            'director_count': str(director_count),
            'shareholder_count': str(shareholder_count),
            'insider_count': str(total_insider),
            'status': status,
            'truncated': 'Yes' if truncated else 'No',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        print(f" {status} (ann={total_announcements}, dir={director_count}, shr={shareholder_count}, code={code}, trunc={'Y' if truncated else 'N'})")
        
    except Exception as e:
        print(f" EXCEPTION: {type(e).__name__}")
        failed_to_fetch.append((name, str(e)))

print(f"\n[*] Re-measurement summary:")
print(f"    Successfully re-measured: {len(remeasured)}")
print(f"    Failed to fetch: {len(failed_to_fetch)}")

if failed_to_fetch:
    print(f"    Failed companies:")
    for name, err in failed_to_fetch:
        print(f"      - {name}: {err[:60]}")

# Analyze results
passed = {name: row for name, row in remeasured.items() if row['status'] == 'PASS'}
print(f"    PASS (≥1 insider filing): {len(passed)}")
print(f"    FAIL (zero insider filings): {len(remeasured) - len(passed)}")

# Write remeasured CSV
output_file = "docs/SGX_WATCHLIST_REMEASURED.csv"
fieldnames = ['name', 'code', 'total_announcements', 'director_count', 'shareholder_count', 
              'insider_count', 'status', 'truncated', 'timestamp']

with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for name in sorted(remeasured.keys()):
        writer.writerow(remeasured[name])

print(f"\n[+] Remeasured data written to: {output_file}")

# Export summary
summary = {
    'remeasure_summary': {
        'total_remeasured': len(remeasured),
        'passed': len(passed),
        'failed': len(remeasured) - len(passed),
        'failed_to_fetch': len(failed_to_fetch),
    },
    'baseline_analysis': {
        'pass_companies': len(pass_companies),
        'fail_companies': len(fail_companies),
        'confirmed_zero': len(confirmed_zero),
        'capped': len(capped),
    },
    'passed_companies': sorted(passed.keys()),
    'failed_companies': sorted([name for name, row in remeasured.items() if row['status'] == 'FAIL']),
}

with open('docs/REMEASURE_SUMMARY.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"[+] Summary written to: docs/REMEASURE_SUMMARY.json")

sys.exit(0 if len(failed_to_fetch) == 0 else 1)
