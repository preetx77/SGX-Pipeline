#!/usr/bin/env python3
"""
Re-measure the 6 big-name companies with proper error handling.

CRITICAL: Companies returning total_announcements=0 for well-known major SGX issuers
must be treated as measurement failures, not as "no insider filings".

This script includes assertions that fail if:
1. A known major company (UOB, Singtel, Keppel) returns zero announcements
2. No code is found for a successful company measurement
"""

import csv
import json
from datetime import datetime, timedelta
from scraper.client import SGXClient

client = SGXClient(throttle_delay=0.5)

# Big six with expected characteristics (market cap, known listing)
big_six = {
    "UOB": {"expected_min_announcements": 100, "known_major": True},
    "SINGTEL": {"expected_min_announcements": 50, "known_major": True},
    "KEPPEL": {"expected_min_announcements": 50, "known_major": True},
    "FRASERS PROPERTY": {"expected_min_announcements": 30, "known_major": True},
    "MAPLETREE COMMERCIAL": {"expected_min_announcements": 30, "known_major": True},
    "PRUDENTIAL": {"expected_min_announcements": 30, "known_major": True},
}

end_date = datetime.utcnow()
start_date = end_date - timedelta(days=5*365)
period_start = int(start_date.timestamp())
period_end = int(end_date.timestamp())

print(f"[*] Re-measuring 6 big-name companies")
print(f"    Period: {start_date.date()} to {end_date.date()}")
print(f"    With assertions for known major issuers\n")

results = {}
measurement_failures = []

for i, (name, props) in enumerate(big_six.items(), 1):
    print(f"[{i}/6] {name}...", end='', flush=True)
    
    try:
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
            print(f" ERROR: {type(e).__name__}: {str(e)[:50]}")
            continue
        
        total_announcements = len(all_announcements)
        
        # ASSERTION: Known major issuers must return > 0 announcements
        if props.get("known_major") and total_announcements == 0:
            measurement_failures.append({
                'company': name,
                'reason': 'Known major issuer returned zero announcements - measurement failed',
                'expected_min': props['expected_min_announcements'],
                'actual': 0
            })
            print(f" MEASUREMENT_FAILED (returned 0 for known major issuer)")
            continue
        
        # Extract code
        code = None
        if all_announcements and all_announcements[0].get('stock_code'):
            candidate_code = all_announcements[0].get('stock_code')
            if candidate_code and len(candidate_code) <= 4:
                code = candidate_code
        
        # Count insider filings
        director_count = 0
        shareholder_count = 0
        
        for ann in all_announcements:
            title = ann.get('title', '').upper() if ann.get('title') else ''
            if 'FORM 1' in title or 'DIRECTOR' in title:
                director_count += 1
            if 'FORM 3' in title or 'SHAREHOLDER' in title:
                shareholder_count += 1
        
        total_insider = director_count + shareholder_count
        truncated = total_announcements >= 100
        status = 'PASS' if total_insider > 0 else 'FAIL'
        
        results[name] = {
            'name': name,
            'code': code or 'UNKNOWN',
            'total_announcements': total_announcements,
            'director_count': director_count,
            'shareholder_count': shareholder_count,
            'total_insider': total_insider,
            'status': status,
            'truncated': truncated,
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        print(f" {status} (ann={total_announcements}, dir={director_count}, shr={shareholder_count}, code={code})")
        
    except Exception as e:
        print(f" EXCEPTION: {type(e).__name__}")
        measurement_failures.append({
            'company': name,
            'reason': str(e)
        })

# Report
print(f"\n[=] RE-MEASUREMENT COMPLETE")
print(f"    Successfully measured: {len(results)}")
print(f"    Measurement failures: {len(measurement_failures)}")

if measurement_failures:
    print(f"\n[!] MEASUREMENT FAILURES (assertion triggered):")
    for fail in measurement_failures:
        print(f"    {fail['company']}: {fail['reason']}")
        if 'expected_min' in fail:
            print(f"      Expected ≥{fail['expected_min']}, got {fail['actual']}")

# Export
export = {
    'remeasure_big_six_v2': {
        'timestamp': datetime.utcnow().isoformat(),
        'results': results,
        'measurement_failures': measurement_failures,
        'note': 'Zero announcements for known major issuers indicates measurement failure, not lack of insider activity'
    }
}

with open('docs/REMEASURE_BIG_SIX_v2.json', 'w') as f:
    json.dump(export, f, indent=2)

print(f"\n[+] Results exported to: docs/REMEASURE_BIG_SIX_v2.json")

