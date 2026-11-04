#!/usr/bin/env python3
"""
Re-measure the 6 dropped big-name companies with exact issuer names.
Uses iter_company_announcements with full pagination to get accurate counts.

Companies:
- UOB (United Overseas Bank Limited)
- Singtel (Singapore Telecommunications Limited)
- Keppel (Keppel Corporation Limited)
- Frasers Property (Frasers Property Limited)
- Mapletree Commercial Trust (Mapletree Commercial Trust)
- Prudential (Prudential plc)
"""

import csv
import json
from datetime import datetime, timedelta
from scraper.client import SGXClient

client = SGXClient(throttle_delay=0.5)

# Exact issuer names to try
big_six = [
    "United Overseas Bank Limited",
    "Singapore Telecommunications Limited",
    "Keppel Corporation Limited",
    "Frasers Property Limited",
    "Mapletree Commercial Trust",
    "Prudential plc",
]

# Time period (5 years)
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=5*365)
period_start = int(start_date.timestamp())
period_end = int(end_date.timestamp())

print(f"[*] Re-measuring 6 big-name companies")
print(f"    Period: {start_date.date()} to {end_date.date()}")
print(f"    Using exact issuer names and iter_company_announcements\n")

results = {}
failed = []

for i, name in enumerate(big_six, 1):
    print(f"[{i}/6] {name}...", end='', flush=True)
    
    try:
        # Fetch all announcements using pagination
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
            failed.append((name, str(e)))
            continue
        
        # Count insider filings (Form 1 = director, Form 3 = shareholder)
        director_count = 0
        shareholder_count = 0
        form1_filings = []
        form3_filings = []
        
        for ann in all_announcements:
            title = ann.get('title', '').upper() if ann.get('title') else ''
            if 'FORM 1' in title or 'DIRECTOR' in title:
                director_count += 1
                form1_filings.append({
                    'title': ann.get('title'),
                    'date': ann.get('announcement_date'),
                    'url': ann.get('url')
                })
            if 'FORM 3' in title or 'SHAREHOLDER' in title:
                shareholder_count += 1
                form3_filings.append({
                    'title': ann.get('title'),
                    'date': ann.get('announcement_date'),
                    'url': ann.get('url')
                })
        
        total_insider = director_count + shareholder_count
        total_announcements = len(all_announcements)
        truncated = total_announcements >= 100
        
        # Try to extract code
        code = None
        if all_announcements and all_announcements[0].get('stock_code'):
            candidate_code = all_announcements[0].get('stock_code')
            if candidate_code and len(candidate_code) <= 4:
                code = candidate_code
        
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
            'form1_sample': form1_filings[:2] if form1_filings else [],
            'form3_sample': form3_filings[:2] if form3_filings else [],
        }
        
        print(f" {status} (ann={total_announcements}, dir={director_count}, shr={shareholder_count}, code={code}, trunc={'Y' if truncated else 'N'})")
        
    except Exception as e:
        print(f" EXCEPTION: {type(e).__name__}")
        failed.append((name, str(e)))

# Summary
print(f"\n[=] RE-MEASUREMENT COMPLETE")
print(f"    Successfully measured: {len(results)}")
print(f"    Failed to fetch: {len(failed)}")

passed = {name: data for name, data in results.items() if data['status'] == 'PASS'}
print(f"    PASS (≥1 insider filing): {len(passed)}")
print(f"    FAIL (zero insider filings): {len(results) - len(passed)}")

if failed:
    print(f"\n[!] Failed companies:")
    for name, err in failed:
        print(f"    - {name}: {err[:50]}")

# Export results
export = {
    'remeasure_big_six': {
        'timestamp': datetime.utcnow().isoformat(),
        'period': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        },
        'results': {name: {k: v for k, v in data.items() if k not in ['form1_sample', 'form3_sample']} 
                   for name, data in results.items()},
        'passed': len(passed),
        'failed': len(results) - len(passed),
    },
    'passed_companies': list(passed.keys()),
    'details': results
}

with open('docs/REMEASURE_BIG_SIX.json', 'w') as f:
    json.dump(export, f, indent=2)

print(f"\n[+] Results exported to: docs/REMEASURE_BIG_SIX.json")

# If any PASS, create CSV row for addition to watchlist
if passed:
    print(f"\n[+] Companies to add back to watchlist:")
    for name, data in passed.items():
        print(f"    {name} ({data['code']}): {data['director_count']} director + {data['shareholder_count']} shareholder filings")

