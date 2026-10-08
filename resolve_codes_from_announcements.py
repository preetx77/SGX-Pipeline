#!/usr/bin/env python3
"""
Resolve actual SGX ticker codes for 401 companies by querying the /company
(announcements) endpoint and extracting stock_code from issuer data.

Strategy:
1. For each of 401 company names, query /company endpoint
2. Extract stock_code from issuers[0] if present
3. Categorize results:
   - RESOLVED: Got a valid code
   - NO_CODE: Company found but no code assigned
   - NO_ANNOUNCEMENTS: Company found but no announcement data
   - ERROR: Query failed
4. Save all 4 categories separately for explicit review
5. Do NOT silently drop or guess—flag everything for decision

Throttling: 1.0 second between requests (proven safe rate from earlier work)
"""

import json
import time
from scraper.client import SGXClient
from datetime import datetime

print("=" * 120)
print("RESOLVE SGX TICKER CODES FOR 401 COMPANIES")
print("=" * 120)

# Load the 401 matched company names
with open('match_results_exact.json', 'r') as f:
    matched_companies = json.load(f)

print(f"\nProcessing {len(matched_companies)} companies...")
print(f"Throttle rate: 1.0 second/request (proven safe)")
print(f"Estimated time: ~{len(matched_companies) / 60:.1f} minutes\n")

# Initialize client with proven throttle rate
client = SGXClient(throttle_delay=1.0)

# Result categories
results = {
    "resolved": [],
    "no_code": [],
    "no_announcements": [],
    "errors": []
}

start_time = time.time()

for i, entry in enumerate(matched_companies):
    company_name = entry['name']
    placeholder_code = entry['placeholder_code']
    
    # Progress indicator
    if (i + 1) % 50 == 0 or (i + 1) == len(matched_companies):
        elapsed = time.time() - start_time
        rate = (i + 1) / elapsed if elapsed > 0 else 0
        print(f"  [{i+1:3d}/{len(matched_companies)}] {company_name[:50]:50s} ({rate:.1f} req/min)")
    
    try:
        # Query for announcements from this company
        params = {
            'value': company_name,
            'pagestart': 0,
            'pagesize': 1
        }
        
        response = client._get('company', params=params)
        
        if not response or 'data' not in response or len(response['data']) == 0:
            # No announcement records found for this company
            results["no_announcements"].append({
                "name": company_name,
                "placeholder_code": placeholder_code,
                "status": "NO_ANNOUNCEMENTS",
                "note": "Company exists in SGX list but has no announcement history"
            })
            continue
        
        # Found announcement data
        record = response['data'][0]
        
        if 'issuers' not in record or len(record['issuers']) == 0:
            results["no_announcements"].append({
                "name": company_name,
                "placeholder_code": placeholder_code,
                "status": "NO_ISSUER_DATA",
                "note": "Announcement record exists but no issuer data"
            })
            continue
        
        # Extract stock code from issuer
        issuer = record['issuers'][0]
        stock_code = issuer.get('stock_code', '').strip()
        returned_name = issuer.get('issuer_name', company_name)
        
        if stock_code:
            # Successfully resolved
            results["resolved"].append({
                "name": company_name,
                "placeholder_code": placeholder_code,
                "stock_code": stock_code,
                "returned_name": returned_name,
                "status": "RESOLVED",
                "source": "announcements_endpoint"
            })
        else:
            # Company found but no stock code assigned
            results["no_code"].append({
                "name": company_name,
                "placeholder_code": placeholder_code,
                "returned_name": returned_name,
                "status": "NO_CODE",
                "note": "Company/security listed but no stock code assigned"
            })
    
    except Exception as e:
        results["errors"].append({
            "name": company_name,
            "placeholder_code": placeholder_code,
            "status": "ERROR",
            "error_message": str(e)
        })

elapsed_time = time.time() - start_time

print(f"\n" + "=" * 120)
print("RESOLUTION RESULTS")
print("=" * 120)
print(f"\nProcessing completed in {elapsed_time:.1f} seconds")
print(f"\nBreakdown:")
print(f"  Resolved (valid codes): {len(results['resolved'])}")
print(f"  No code assigned: {len(results['no_code'])}")
print(f"  No announcement history: {len(results['no_announcements'])}")
print(f"  Errors: {len(results['errors'])}")
print(f"  Total: {sum(len(v) for v in results.values())}")

# Save detailed results
print(f"\nSaving results files...")

if results['resolved']:
    with open('codes_resolved.json', 'w') as f:
        json.dump(results['resolved'], f, indent=2)
    print(f"  ✓ codes_resolved.json ({len(results['resolved'])} entries)")

if results['no_code']:
    with open('codes_empty.json', 'w') as f:
        json.dump(results['no_code'], f, indent=2)
    print(f"  ✓ codes_empty.json ({len(results['no_code'])} entries - REQUIRES DECISION)")

if results['no_announcements']:
    with open('codes_no_announcements.json', 'w') as f:
        json.dump(results['no_announcements'], f, indent=2)
    print(f"  ✓ codes_no_announcements.json ({len(results['no_announcements'])} entries - REQUIRES DECISION)")

if results['errors']:
    with open('codes_errors.json', 'w') as f:
        json.dump(results['errors'], f, indent=2)
    print(f"  ✓ codes_errors.json ({len(results['errors'])} entries - REQUIRES REVIEW)")

print(f"\n" + "=" * 120)
print("NEXT STEPS")
print("=" * 120)
print(f"""
1. Review codes_resolved.json: {len(results['resolved'])} companies ready for Stage 5

2. DECISION REQUIRED on edge cases:
   - codes_empty.json ({len(results['no_code'])} entries):
     Companies listed with no stock code. Include or exclude from Stage 5?
   
   - codes_no_announcements.json ({len(results['no_announcements'])} entries):
     Companies exist but have no announcement history. Include or exclude?
   
   - codes_errors.json ({len(results['errors'])} entries):
     Query failures. Investigate or exclude?

3. Spot-check 3 RESOLVED codes against SGX public site (independent verification)

4. Build final watchlist_500_real.py with decision on edge cases

5. Launch Stage 5 with verified, coded company list
""")

print("=" * 120)

