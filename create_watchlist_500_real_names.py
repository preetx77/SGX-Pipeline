#!/usr/bin/env python3
"""
Create a 500-company watchlist using:
1. The 99 existing real companies (with verified codes)
2. 401 real company NAMES from SGX /companylist endpoint
   (Codes will be placeholder format "SGX_REAL_001" etc. pending proper ticker discovery)

This eliminates the obviously fake "SGX LISTED COMPANY" entries while we work on
getting actual ticker codes for the additional companies.
"""

from scraper.client import SGXClient
import re

print("=" * 120)
print("CREATE 500-COMPANY WATCHLIST WITH REAL NAMES (PLACEHOLDER CODES PENDING)")
print("=" * 120)

# Fetch SGX company list
print("\nFetching SGX company list...")
client = SGXClient()
try:
    response = client.get_company_list()
    company_names = response['data']
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

print(f"Total companies available: {len(company_names)}")

# Read existing watchlist_500.py to extract real companies with codes
print("\nExtracting existing real companies...")
with open('config/watchlist_500.py', 'r') as f:
    watchlist_content = f.read()

real_company_pattern = r'Company\(\s*name="([^"]+)",\s*code="([^"]+)"'
all_matches = re.findall(real_company_pattern, watchlist_content)

existing_real_companies = []
existing_names = set()
existing_codes = set()

for name, code in all_matches:
    if not name.startswith("SGX LISTED COMPANY"):
        existing_real_companies.append((name, code))
        existing_names.add(name.upper())
        existing_codes.add(code.upper())

print(f"Existing real companies with verified codes: {len(existing_real_companies)}")

# Find new companies from SGX list that we don't already have
print(f"\nSearching for {500 - len(existing_real_companies)} additional real companies...")
additional_companies = []

for sgx_name in company_names:
    if sgx_name.upper() not in existing_names and len(additional_companies) < (500 - len(existing_real_companies)):
        additional_companies.append(sgx_name)

print(f"Found {len(additional_companies)} additional real company names")

# Generate temporary code for new companies (format: SGX_REAL_001, SGX_REAL_002, etc.)
# These are placeholders until we can map actual SGX ticker codes
additional_with_codes = []
for i, name in enumerate(additional_companies, 1):
    code = f"SGX_REAL_{i:04d}"
    additional_with_codes.append((name, code))

# Generate the new watchlist file
print(f"\nGenerating watchlist_500_real_names.py...")

new_watchlist = '''from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5: 500-company watchlist (REAL NAMES, PLACEHOLDER CODES)
# 
# Composition:
#   - 99 existing companies with verified SGX ticker codes
#   - 401 additional companies with real names from SGX /companylist
#     (using placeholder codes SGX_REAL_0001..0401 pending ticker code discovery)
#
# IMPORTANT: This watchlist has real company NAMES but placeholder codes for the additional 401.
# The system will need ticket code mapping or the new companies will error on API calls.
# See: WATCHLIST_500_REAL_NAMES_STATUS.md for migration plan.

WATCHLIST = [
'''

# Add existing real companies (with real codes)
for name, code in existing_real_companies:
    new_watchlist += f'''    Company(
        name="{name}",
        code="{code}",
        priority="normal",
        sector="Unknown",
    ),
'''

# Add new companies (with placeholder codes)
for name, code in additional_with_codes:
    new_watchlist += f'''    Company(
        name="{name}",
        code="{code}",
        priority="normal",
        sector="Unknown",
    ),
'''

new_watchlist += ''']\n'''

# Write output
with open('config/watchlist_500_real_names.py', 'w') as f:
    f.write(new_watchlist)

print(f"✓ Created config/watchlist_500_real_names.py")

# Create a status document
status = f'''# Watchlist 500 Real Names Status

## Issue
The initial watchlist_500.py contained 401 fake placeholder entries (SGX LISTED COMPANY 101-500)
instead of real SGX-listed companies. This invalidated all Stage 5 measurements.

## Solution Status
- ✓ Created watchlist_500_real_names.py with 99 verified + 401 real company names
- ⏳ PENDING: Map real SGX ticker codes to the 401 new companies

## Current State
- 99 companies: Real names + verified SGX ticker codes (READY)
- 401 companies: Real names + placeholder codes SGX_REAL_0001..0401 (NOT YET USABLE)

## To Proceed
The 401 placeholder codes must be replaced with actual SGX ticker codes before Stage 5 can run.
Options:
1. Query SGX API individually for each company name to get the ticker code
2. Manually map the 401 company names to their SGX codes
3. Accept a 99-company Stage 5 until codes are obtained

## Action Required
Pick one of the above approaches and update watchlist_500_real_names.py before restarting Stage 5.

Generated: 2026-10-07
Watchlist file: config/watchlist_500_real_names.py
Existing code: 99 companies
New code: 401 companies (placeholder SGX_REAL_XXXX codes)
Total: 500 companies
'''

with open('WATCHLIST_500_REAL_NAMES_STATUS.md', 'w') as f:
    f.write(status)

print(f"✓ Created WATCHLIST_500_REAL_NAMES_STATUS.md")
print(f"\nSummary:")
print(f"  Real companies with codes: {len(existing_real_companies)}")
print(f"  Real companies with placeholder codes: {len(additional_with_codes)}")
print(f"  Total: {len(existing_real_companies) + len(additional_with_codes)}")
print(f"\nNext step: Map SGX ticker codes to the 401 new company names")

