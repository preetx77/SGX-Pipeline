#!/usr/bin/env python3
"""
Generate a proper 500-company watchlist using real SGX-listed companies.
Replaces all fake "SGX LISTED COMPANY" placeholders with actual verified tickers.

Process:
1. Fetch full company list from SGX /companylist endpoint
2. Keep the existing 99 real companies (baseline + Stage 4.5 expansion)
3. Add 401 additional real companies from the SGX list to reach 500
4. Generate watchlist_500_real.py with verified companies
"""

import sys
import json
from scraper.client import SGXClient

print("=" * 120)
print("GENERATE REAL 500-COMPANY WATCHLIST FOR STAGE 5")
print("=" * 120)

# Initialize client and fetch company list
print("\nFetching SGX company list...")
client = SGXClient()

try:
    company_data = client.get_company_list()
except Exception as e:
    print(f"ERROR: Failed to fetch company list: {e}")
    sys.exit(1)

# Parse the response
if isinstance(company_data, dict) and 'data' in company_data:
    companies = company_data['data']
elif isinstance(company_data, list):
    companies = company_data
else:
    print(f"ERROR: Unexpected company list format: {type(company_data)}")
    print(f"Raw response: {company_data}")
    sys.exit(1)

print(f"Total companies available from SGX: {len(companies)}")

# Read existing watchlist_500.py to extract real companies
print("\nReading existing watchlist_500.py...")
with open('config/watchlist_500.py', 'r') as f:
    watchlist_content = f.read()

# Extract real companies (non-placeholder entries)
import re
real_company_pattern = r'Company\(\s*name="([^"]+)",\s*code="([^"]+)"'
all_matches = re.findall(real_company_pattern, watchlist_content)

existing_real_companies = []
existing_codes = set()

for name, code in all_matches:
    if not name.startswith("SGX LISTED COMPANY"):
        existing_real_companies.append((name, code))
        existing_codes.add(code.upper())

print(f"Existing real companies in watchlist: {len(existing_real_companies)}")
print(f"Need to add: {500 - len(existing_real_companies)} more real companies")

# Extract real companies from SGX list that we don't already have
additional_needed = 500 - len(existing_real_companies)
candidates = []

for company in companies:
    # SGX returns: {'code': 'XXX', 'name': 'Company Name', ...}
    code = company.get('code', '').upper().strip()
    name = company.get('name', '').strip()
    
    if not code or not name:
        continue
    
    if code not in existing_codes:
        candidates.append((name, code))
        if len(candidates) >= additional_needed:
            break

print(f"Found {len(candidates)} additional real companies from SGX")

if len(candidates) < additional_needed:
    print(f"\nWARNING: Only found {len(candidates)}, needed {additional_needed}")
    print("SGX company list may be incomplete or API response format is different.")
    print(f"Response sample (first 3 entries): {json.dumps(companies[:3], indent=2)}")
    sys.exit(1)

# Generate the new watchlist
print(f"\nGenerating watchlist_500_real.py with {len(existing_real_companies) + len(candidates)} real companies...")

new_watchlist = '''from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5: 500-company watchlist (REAL COMPANIES ONLY)
# Composition: 99 (existing real) + 401 (additional real from SGX companylist)
# Total: 500 unique, verified SGX-listed companies
#
# Verify: No duplicates via: set(c.code for c in WATCHLIST)
# Verify: All real companies via SGX /companylist endpoint

WATCHLIST = [
'''

# Add existing real companies
for name, code in existing_real_companies:
    new_watchlist += f'''    Company(
        name="{name}",
        code="{code}",
        priority="normal",
        sector="Unknown",
    ),
'''

# Add new real companies
for name, code in candidates:
    new_watchlist += f'''    Company(
        name="{name}",
        code="{code}",
        priority="normal",
        sector="Unknown",
    ),
'''

new_watchlist += ''']\n'''

# Write to watchlist_500_real.py
output_file = 'config/watchlist_500_real.py'
with open(output_file, 'w') as f:
    f.write(new_watchlist)

print(f"✓ Created {output_file}")
print(f"\nSummary:")
print(f"  Existing real companies: {len(existing_real_companies)}")
print(f"  New real companies added: {len(candidates)}")
print(f"  Total in new watchlist: {len(existing_real_companies) + len(candidates)}")
print(f"\nNext steps:")
print(f"1. Review the generated {output_file}")
print(f"2. Verify no duplicate codes: python -c \"from config.watchlist_500_real import WATCHLIST; codes = [c.code for c in WATCHLIST]; print('Duplicates:', [c for c in codes if codes.count(c) > 1] or 'None')\"")
print(f"3. Update run_system.py to import from watchlist_500_real instead of watchlist_500")
print(f"4. Restart Stage 5 with real companies")

print("\n" + "=" * 120)

