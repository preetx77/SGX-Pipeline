#!/usr/bin/env python3
"""Fixed version: handle None responses gracefully"""

import json
import time
from scraper.client import SGXClient

# Load the 401 matched companies
with open('match_results_exact.json', 'r') as f:
    matched_companies = json.load(f)

# Load existing results
try:
    with open('codes_resolved.json', 'r') as f:
        resolved = json.load(f)
    with open('codes_empty.json', 'r') as f:
        no_code = json.load(f)
    with open('codes_no_announcements.json', 'r') as f:
        no_announcements = json.load(f)
    with open('codes_errors.json', 'r') as f:
        errors = json.load(f)
    processed_names = {e['name'] for e in resolved + no_code + no_announcements + errors}
except:
    resolved = []
    no_code = []
    no_announcements = []
    errors = []
    processed_names = set()

remaining = [c for c in matched_companies if c['name'] not in processed_names]

if remaining:
    batch = remaining[:50]
    client = SGXClient(throttle_delay=1.0)
    
    for i, entry in enumerate(batch):
        company_name = entry['name']
        placeholder_code = entry['placeholder_code']
        
        try:
            params = {'value': company_name, 'pagestart': 0, 'pagesize': 1}
            response = client._get('company', params=params)
            
            # Handle None response
            if not response:
                no_announcements.append({
                    "name": company_name,
                    "placeholder_code": placeholder_code,
                    "status": "NO_DATA",
                })
                continue
            
            if 'data' not in response or response['data'] is None or len(response['data']) == 0:
                no_announcements.append({
                    "name": company_name,
                    "placeholder_code": placeholder_code,
                    "status": "NO_ANNOUNCEMENTS",
                })
                continue
            
            record = response['data'][0]
            if not record or 'issuers' not in record or record['issuers'] is None or len(record['issuers']) == 0:
                no_announcements.append({
                    "name": company_name,
                    "placeholder_code": placeholder_code,
                    "status": "NO_ISSUER_DATA",
                })
                continue
            
            issuer = record['issuers'][0]
            stock_code = issuer.get('stock_code', '').strip() if issuer else ''
            returned_name = issuer.get('issuer_name', company_name) if issuer else company_name
            
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
    with open('codes_resolved.json', 'w') as f:
        json.dump(resolved, f, indent=2)
    with open('codes_empty.json', 'w') as f:
        json.dump(no_code, f, indent=2)
    with open('codes_no_announcements.json', 'w') as f:
        json.dump(no_announcements, f, indent=2)
    with open('codes_errors.json', 'w') as f:
        json.dump(errors, f, indent=2)
    
    print(f"Processed {len(batch)} companies")
    print(f"  Resolved: {len(resolved)}, No code: {len(no_code)}, No data: {len(no_announcements)}, Errors: {len(errors)}")
    
    remaining_after = 401 - (len(resolved) + len(no_code) + len(no_announcements) + len(errors))
    if remaining_after > 0:
        print(f"Remaining: {remaining_after}")

