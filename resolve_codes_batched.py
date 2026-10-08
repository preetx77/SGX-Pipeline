#!/usr/bin/env python3
"""
Resolve SGX codes in batches (50 at a time), resumable, with explicit edge case tracking.
"""

import json
import time
from scraper.client import SGXClient

print("=" * 120)
print("RESOLVE SGX CODES - BATCHED PROCESSING")
print("=" * 120)

# Load the 401 matched companies
with open('match_results_exact.json', 'r') as f:
    matched_companies = json.load(f)

# Check if we have partial results
try:
    with open('codes_resolved.json', 'r') as f:
        resolved = json.load(f)
    with open('codes_empty.json', 'r') as f:
        no_code = json.load(f)
    with open('codes_no_announcements.json', 'r') as f:
        no_announcements = json.load(f)
    with open('codes_errors.json', 'r') as f:
        errors = json.load(f)
    print(f"Resuming from previous run...")
    processed_names = {e['name'] for e in resolved + no_code + no_announcements + errors}
except:
    resolved = []
    no_code = []
    no_announcements = []
    errors = []
    processed_names = set()

# Get remaining companies
remaining = [c for c in matched_companies if c['name'] not in processed_names]
print(f"Already processed: {len(processed_names)}")
print(f"Remaining: {len(remaining)}")

if not remaining:
    print("All companies processed!")
else:
    # Process first batch of 50
    batch_size = 50
    batch = remaining[:batch_size]
    
    print(f"\nProcessing batch of {len(batch)} companies (1 sec throttle)...")
    client = SGXClient(throttle_delay=1.0)
    
    for i, entry in enumerate(batch):
        company_name = entry['name']
        placeholder_code = entry['placeholder_code']
        
        if (i + 1) % 10 == 0:
            print(f"  [{i+1:2d}/{len(batch)}] {company_name[:50]}")
        
        try:
            params = {'value': company_name, 'pagestart': 0, 'pagesize': 1}
            response = client._get('company', params=params)
            
            if not response or 'data' not in response or len(response['data']) == 0:
                no_announcements.append({
                    "name": company_name,
                    "placeholder_code": placeholder_code,
                    "status": "NO_ANNOUNCEMENTS",
                })
                continue
            
            record = response['data'][0]
            if 'issuers' not in record or len(record['issuers']) == 0:
                no_announcements.append({
                    "name": company_name,
                    "placeholder_code": placeholder_code,
                    "status": "NO_ISSUER_DATA",
                })
                continue
            
            issuer = record['issuers'][0]
            stock_code = issuer.get('stock_code', '').strip()
            returned_name = issuer.get('issuer_name', company_name)
            
            if stock_code:
                resolved.append({
                    "name": company_name,
                    "placeholder_code": placeholder_code,
                    "stock_code": stock_code,
                    "returned_name": returned_name,
                    "status": "RESOLVED",
                })
            else:
                no_code.append({
                    "name": company_name,
                    "placeholder_code": placeholder_code,
                    "returned_name": returned_name,
                    "status": "NO_CODE",
                })
        
        except Exception as e:
            errors.append({
                "name": company_name,
                "placeholder_code": placeholder_code,
                "status": "ERROR",
                "error": str(e)[:100],
            })
    
    # Save results
    print(f"\nSaving batch results...")
    with open('codes_resolved.json', 'w') as f:
        json.dump(resolved, f, indent=2)
    with open('codes_empty.json', 'w') as f:
        json.dump(no_code, f, indent=2)
    with open('codes_no_announcements.json', 'w') as f:
        json.dump(no_announcements, f, indent=2)
    with open('codes_errors.json', 'w') as f:
        json.dump(errors, f, indent=2)
    
    print(f"\nBatch complete. Results saved.")
    print(f"  Resolved: {len(resolved)}")
    print(f"  No code: {len(no_code)}")
    print(f"  No announcements: {len(no_announcements)}")
    print(f"  Errors: {len(errors)}")
    print(f"\nRun again to process next batch.")

