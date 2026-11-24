#!/usr/bin/env python3
"""
Expand watchlist from 32 to 100 companies using corrected dates.

Fixes system date issue by using date override from config/date_override.py
"""

import csv
import json
import sys
sys.path.insert(0, '.')

from datetime import timedelta
from scraper.client import SGXClient
from config.date_override import get_api_query_dates
from config.watchlist import WATCHLIST

client = SGXClient(throttle_delay=1.0)

# Get corrected date range
dates = get_api_query_dates(lookback_days=1825)
period_start = dates['period_start']
period_end = dates['period_end']
start_date = dates['start']
end_date = dates['end']

print(f"[*] WATCHLIST EXPANSION: 32 → 100 COMPANIES")
print(f"{'='*80}\n")
print(f"Using corrected dates:")
print(f"  Period: {start_date.date()} to {end_date.date()}")
print(f"  Current: {len(WATCHLIST)} companies")
print(f"  Target: 100 companies")
print(f"  Need: {100 - len(WATCHLIST)} more\n")

# Load current watchlist
current_names = {c.name for c in WATCHLIST}
current_codes = {c.code for c in WATCHLIST}

# Expansion candidates (well-known SGX companies)
expansion_candidates = [
    "Singapore Exchange Limited",
    "Genting Singapore Limited",
    "Wilmar International Limited",
    "City Developments Limited",
    "CapitaLand Integration Limited",
    "Singapore Airlines Limited",
    "Oversea-Chinese Banking Corporation Limited",
    "United Overseas Bank Limited",
    "Singapore Telecommunications Limited",
    "Keppel Corporation Limited",
    "Frasers Property Limited",
    "Mapletree Commercial Trust",
    "Sheng Siong Group Ltd",
    "Golden Agri-Resources Ltd",
    "United Test & Assembly Centre Ltd",
    "Seatrium Limited",
    "Jiutian Chemical Group Limited",
    "China Jo-Jo Drugstores Inc",
    "Stamford Tyres Corporation Ltd",
    "ISIG Holdings Limited",
]

# Measure candidates
measured = {
    'pass': [],
    'fail': [],
}

print(f"Measuring {len(expansion_candidates)} expansion candidates...\n")

for i, name in enumerate(expansion_candidates, 1):
    # Skip if already in watchlist
    if name in current_names:
        print(f"[{i:2d}] {name[:50]:50s} SKIP (in watchlist)")
        continue
    
    print(f"[{i:2d}] {name[:50]:50s}", end='', flush=True)
    
    try:
        # Measure with corrected dates
        all_announcements = []
        for ann in client.iter_company_announcements(name, period_start, period_end, page_size=100):
            all_announcements.append(ann)
        
        # Count filings
        director_count = sum(1 for a in all_announcements 
                            if 'FORM 1' in (a.get('title', '') or '').upper())
        total_insider = director_count
        
        # Get code
        code = None
        if all_announcements and all_announcements[0].get('stock_code'):
            candidate_code = all_announcements[0].get('stock_code')
            if candidate_code and len(candidate_code) <= 4 and candidate_code not in current_codes:
                code = candidate_code
        
        result = {
            'name': name,
            'code': code or 'UNKNOWN',
            'announcements': len(all_announcements),
            'director_filings': director_count,
            'status': 'PASS' if total_insider > 0 else 'FAIL',
        }
        
        if result['status'] == 'PASS':
            measured['pass'].append(result)
            print(f" PASS ({director_count} director filings, code={code})")
        else:
            measured['fail'].append(result)
            print(f" FAIL ({len(all_announcements)} announcements)")
        
    except Exception as e:
        print(f" ERROR: {type(e).__name__}")

# Summary
print(f"\n{'='*80}")
print(f"\n[=] EXPANSION MEASUREMENT SUMMARY")
print(f"    PASS candidates: {len(measured['pass'])}")
print(f"    FAIL candidates: {len(measured['fail'])}")

pass_needed = 100 - len(WATCHLIST)
pass_available = len(measured['pass'])

print(f"\n[*] EXPANSION PLAN")
print(f"    Need: {pass_needed} more companies")
print(f"    Available PASS: {pass_available}")

if pass_available >= pass_needed:
    print(f"    Status: CAN REACH 100 ✓")
else:
    print(f"    Status: Need more candidates ({pass_needed - pass_available} shortfall)")

if measured['pass']:
    print(f"\n[+] CANDIDATES FOR EXPANSION:")
    for cand in sorted(measured['pass'], key=lambda x: x['director_filings'], reverse=True):
        print(f"    {cand['name'][:50]:50s} ({cand['director_filings']} filings, code={cand['code']})")

# Export
export = {
    'timestamp': end_date.isoformat(),
    'period': {
        'start': start_date.isoformat(),
        'end': end_date.isoformat(),
    },
    'current_count': len(WATCHLIST),
    'target_count': 100,
    'pass_count': len(measured['pass']),
    'fail_count': len(measured['fail']),
    'pass_candidates': sorted(measured['pass'], 
                             key=lambda x: x['director_filings'], 
                             reverse=True),
    'fail_candidates': measured['fail'],
}

with open('docs/EXPANSION_V2_RESULTS.json', 'w') as f:
    json.dump(export, f, indent=2)

print(f"\n[+] Results saved to: docs/EXPANSION_V2_RESULTS.json")

