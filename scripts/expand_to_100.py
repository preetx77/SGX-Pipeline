#!/usr/bin/env python3
"""
Expand watchlist from 32 to 100 companies by measuring SGX listings.

Strategy:
1. Load current 32 (baseline)
2. Measure SGX companies systematically from a large pool
3. Identify all PASS companies (≥1 director filing)
4. Add top 68 by insider filing count
5. Update watchlist.py and measurement CSV
"""

import csv
import json
from datetime import datetime, timedelta
from scraper.client import SGXClient
from collections import defaultdict

client = SGXClient(throttle_delay=1.0)

# Load current watchlist
from config.watchlist import WATCHLIST
current_names = {c.name for c in WATCHLIST}
current_codes = {c.code for c in WATCHLIST}

print(f"[*] WATCHLIST EXPANSION: 32 → 100 COMPANIES")
print(f"{'='*80}\n")
print(f"Current: {len(WATCHLIST)} companies")
print(f"Target: 100 companies")
print(f"Need: {100 - len(WATCHLIST)} more\n")

# Time period
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=5*365)
period_start = int(start_date.timestamp())
period_end = int(end_date.timestamp())

# Candidates: Common SGX companies by market cap / volume
# (These are well-known SGX listings likely to have insider activity)
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
    "Seatrade Limited",
    "AMTD International Inc",
    "Luokung Technology Corp",
    "China SinoHub Inc",
    "Golden Energy and Resources Limited",
    "Asia Pacific Wire & Cable Corporation Limited",
    "Full House Resorts Inc",
    "China Commercial Credit Inc",
    "China HGS Real Estate Inc",
    "China Shenghuo Greenenergia Limited",
    # Add more as needed
]

# Measure candidates
measured = {
    'pass': [],
    'fail': [],
    'skip': [],
}

print(f"Measuring {len(expansion_candidates)} expansion candidates...\n")

for i, name in enumerate(expansion_candidates, 1):
    # Skip if already in watchlist
    if name in current_names:
        measured['skip'].append(name)
        print(f"[{i:2d}] {name[:50]:50s} SKIP")
        continue
    
    print(f"[{i:2d}] {name[:50]:50s}", end='', flush=True)
    
    try:
        # Measure
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
            print(f" PASS ({director_count} director filings)")
        else:
            measured['fail'].append(result)
            print(f" FAIL")
        
    except Exception as e:
        print(f" ERROR: {type(e).__name__}")

# Summary
print(f"\n{'='*80}")
print(f"\n[=] EXPANSION MEASUREMENT SUMMARY")
print(f"    PASS candidates: {len(measured['pass'])}")
print(f"    FAIL candidates: {len(measured['fail'])}")
print(f"    Already in watchlist: {len(measured['skip'])}")

# Calculate how many we need
pass_needed = 100 - len(WATCHLIST)
pass_available = len(measured['pass'])

print(f"\n[*] EXPANSION PLAN")
print(f"    Need: {pass_needed} more companies")
print(f"    Available PASS: {pass_available}")

if pass_available >= pass_needed:
    print(f"    Status: CAN REACH 100 ✓")
    # Sort by director filings (descending)
    top_candidates = sorted(measured['pass'], 
                           key=lambda x: x['director_filings'], 
                           reverse=True)[:pass_needed]
    print(f"\n[+] TOP {pass_needed} CANDIDATES:")
    for j, cand in enumerate(top_candidates, 1):
        print(f"    {j:2d}. {cand['name'][:50]:50s} ({cand['director_filings']} filings, code={cand['code']})")
else:
    shortfall = pass_needed - pass_available
    print(f"    Status: SHORTFALL OF {shortfall} companies")
    print(f"    Need to measure more from SGX top 500")

# Export
export = {
    'timestamp': datetime.utcnow().isoformat(),
    'current_count': len(WATCHLIST),
    'target_count': 100,
    'pass_count': len(measured['pass']),
    'fail_count': len(measured['fail']),
    'pass_candidates': sorted(measured['pass'], 
                             key=lambda x: x['director_filings'], 
                             reverse=True),
}

with open('docs/EXPANSION_CANDIDATES_MEASURED.json', 'w') as f:
    json.dump(export, f, indent=2)

print(f"\n[+] Results saved to: docs/EXPANSION_CANDIDATES_MEASURED.json")

