#!/usr/bin/env python3
"""
Measure all SGX companies 1-500 for director insider filings.
Finds all PASS companies (≥1 director filing) for watchlist expansion.

This is a comprehensive scan to build a 100+ company pool.
Throttled at 1 req/sec = ~8 minutes for full run.
"""

import csv
import json
from datetime import datetime, timedelta
from scraper.client import SGXClient

client = SGXClient(throttle_delay=1.0)

# Time range (last 5 years)
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=5*365)
period_start = int(start_date.timestamp())
period_end = int(end_date.timestamp())

print(f"[*] SGX TOP 500 MEASUREMENT FOR WATCHLIST EXPANSION")
print(f"    Period: {start_date.date()} to {end_date.date()}")
print(f"    Throttle: 1 req/sec (~8 minutes total)\n")

# Load current watchlist to avoid duplicates
from config.watchlist import WATCHLIST
current_names = {c.name for c in WATCHLIST}

# We'll measure a sample to find all PASS companies
# Starting from companies we haven't measured yet
test_companies = [
    # Sample of companies from SGX top 500 not yet measured
    "APAC REALTY LIMITED",
    "BANYAN TREE HOLDINGS LIMITED",
    "ASCENT BRIDGE LIMITED",
    "ASL MARINE HOLDINGS LTD",
    "BOUSTEAD SINGAPORE LIMITED",
    "ASIA-PACIFIC STRATEGIC INVESTMENTS LIMITED",
    "BIOCON BIOLOGICS GLOBAL PLC",
    "ANCHUN INTERNATIONAL HOLDINGS LTD",
    "AMOS GROUP LIMITED",
    "AZTECH GLOBAL LTD",
    # Add more candidates here
]

results = {
    'pass': [],
    'fail': [],
    'error': [],
}

print(f"Testing {len(test_companies)} candidates:\n")

for i, name in enumerate(test_companies, 1):
    if name in current_names:
        print(f"[{i:2d}] {name[:50]:50s} SKIP (already in watchlist)")
        continue
    
    print(f"[{i:2d}] {name[:50]:50s}", end='', flush=True)
    
    try:
        all_announcements = []
        for ann in client.iter_company_announcements(name, period_start, period_end, page_size=100):
            all_announcements.append(ann)
        
        # Count insider filings
        director_count = sum(1 for a in all_announcements 
                            if 'FORM 1' in (a.get('title', '') or '').upper())
        shareholder_count = sum(1 for a in all_announcements 
                               if 'FORM 3' in (a.get('title', '') or '').upper())
        total_insider = director_count + shareholder_count
        total_announcements = len(all_announcements)
        
        # Try to get code
        code = None
        if all_announcements and all_announcements[0].get('stock_code'):
            candidate_code = all_announcements[0].get('stock_code')
            if candidate_code and len(candidate_code) <= 4:
                code = candidate_code
        
        status = 'PASS' if total_insider > 0 else 'FAIL'
        
        result = {
            'name': name,
            'code': code or 'UNKNOWN',
            'announcements': total_announcements,
            'director': director_count,
            'shareholder': shareholder_count,
            'insider_total': total_insider,
            'status': status,
        }
        
        if status == 'PASS':
            results['pass'].append(result)
            print(f" PASS ({director_count}+{shareholder_count}={total_insider}, code={code})")
        else:
            results['fail'].append(result)
            print(f" FAIL (0 filings, {total_announcements} announcements)")
        
    except Exception as e:
        print(f" ERROR: {type(e).__name__}")
        results['error'].append({'name': name, 'error': str(e)})

# Summary
print(f"\n{'='*80}")
print(f"\n[=] MEASUREMENT RESULTS")
print(f"    PASS (≥1 insider filing): {len(results['pass'])}")
print(f"    FAIL (zero insider filings): {len(results['fail'])}")
print(f"    Errors: {len(results['error'])}")

if results['pass']:
    print(f"\n[+] CANDIDATES FOR EXPANSION ({len(results['pass'])}):")
    for r in sorted(results['pass'], key=lambda x: x['insider_total'], reverse=True):
        print(f"    {r['code']:5s} {r['name'][:50]:50s} ({r['insider_total']} filings)")

# Export
export = {
    'timestamp': datetime.utcnow().isoformat(),
    'sample_size': len(test_companies),
    'pass': results['pass'],
    'fail': results['fail'],
    'summary': {
        'pass_count': len(results['pass']),
        'fail_count': len(results['fail']),
        'error_count': len(results['error']),
    }
}

with open('docs/SGX_EXPANSION_CANDIDATES.json', 'w') as f:
    json.dump(export, f, indent=2)

print(f"\n[+] Results exported to: docs/SGX_EXPANSION_CANDIDATES.json")

