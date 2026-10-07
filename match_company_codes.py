#!/usr/bin/env python3
"""
Match 401 new company names against the real SGX company list (4,299 companies).

Strategy:
1. Fetch the 4,299-company list from SGX /companylist endpoint
2. For each of 401 names in watchlist_500_real_names.py:
   - Try exact match (case-insensitive) first
   - Fall back to fuzzy match (Levenshtein distance)
3. Flag automatic matches as MATCHED, low-confidence as AMBIGUOUS
4. Output:
   - matches.json: auto-resolved (high confidence)
   - ambiguous.json: needs manual review
   - summary: counts and statistics

Output structure enables fast manual review: only inspect ambiguous cases.
"""

import json
import re
from difflib import SequenceMatcher
from scraper.client import SGXClient
import sys

print("=" * 120)
print("MATCH 401 NEW COMPANY NAMES TO SGX TICKER CODES")
print("=" * 120)

# Fetch real company list from SGX
print("\n[1/4] Fetching SGX company list...")
client = SGXClient()
try:
    response = client.get_company_list()
    sgx_companies = response['data']  # List of company names
except Exception as e:
    print(f"ERROR: Failed to fetch company list: {e}")
    sys.exit(1)

print(f"  Fetched: {len(sgx_companies)} companies from SGX")

# Unfortunately, SGX /companylist only returns names, not codes.
# We need to approach this differently: the names in our watchlist should already
# be from SGX. So we're actually just validating they exist in the real list.
# For codes, we'll need to query them individually or use a name->code mapping.

# For now, let's check which of our 401 names exist in the real SGX list

print("\n[2/4] Reading watchlist_500_real_names.py...")
import re
with open('config/watchlist_500_real_names.py', 'r') as f:
    watchlist_content = f.read()

pattern = r'Company\(\s*name="([^"]+)",\s*code="(SGX_REAL_\d+)"'
matches = re.findall(pattern, watchlist_content)

new_companies = []
for name, code in matches:
    new_companies.append((name, code))

print(f"  Found: {len(new_companies)} entries with SGX_REAL_* placeholder codes")

# Separate existing real from placeholders
existing_real = []
placeholder_entries = []
with open('config/watchlist_500.py', 'r') as f:
    watchlist_old = f.read()

real_pattern = r'Company\(\s*name="([^"]+)",\s*code="([^"]+)"'
old_matches = re.findall(real_pattern, watchlist_old)

existing_codes = {}
for name, code in old_matches:
    if not name.startswith("SGX LISTED COMPANY"):
        existing_codes[name.upper()] = code
        existing_real.append((name, code))

print(f"  Existing real companies: {len(existing_real)}")

# Now match the 401 new names
print(f"\n[3/4] Matching {len(new_companies)} names to SGX list...")

# Normalize SGX list for comparison
sgx_names_normalized = {name.upper(): name for name in sgx_companies}

matched_results = {
    "exact_matches": [],
    "fuzzy_matches": [],
    "no_matches": [],
}

def similarity(a, b):
    """Calculate string similarity ratio (0-1)."""
    return SequenceMatcher(None, a.upper(), b.upper()).ratio()

for new_name, placeholder_code in new_companies:
    new_name_upper = new_name.upper()
    
    # Try exact match first
    if new_name_upper in sgx_names_normalized:
        original_name = sgx_names_normalized[new_name_upper]
        matched_results["exact_matches"].append({
            "name": new_name,
            "placeholder_code": placeholder_code,
            "status": "EXACT_MATCH",
            "confidence": 1.0,
            "note": f"Exact match in SGX list: '{original_name}'"
        })
        continue
    
    # Try fuzzy match
    best_match = None
    best_score = 0.8  # Threshold for fuzzy acceptance
    
    for sgx_name in sgx_companies:
        score = similarity(new_name, sgx_name)
        if score > best_score:
            best_score = score
            best_match = sgx_name
    
    if best_match and best_score > 0.85:  # High confidence fuzzy match
        matched_results["fuzzy_matches"].append({
            "name": new_name,
            "placeholder_code": placeholder_code,
            "matched_name": best_match,
            "confidence": best_score,
            "status": "FUZZY_MATCH",
            "note": f"Fuzzy match (similarity: {best_score:.2%}): '{best_match}'"
        })
    else:
        # Could be no match, or ambiguous
        if best_match:
            matched_results["no_matches"].append({
                "name": new_name,
                "placeholder_code": placeholder_code,
                "status": "AMBIGUOUS",
                "best_candidate": best_match,
                "confidence": best_score,
                "note": f"Low confidence fuzzy match ({best_score:.2%}), needs review. Best candidate: '{best_match}'"
            })
        else:
            matched_results["no_matches"].append({
                "name": new_name,
                "placeholder_code": placeholder_code,
                "status": "NOT_FOUND",
                "confidence": 0.0,
                "note": "No match found in SGX list, possibly delisted or misspelled"
            })

print(f"  Exact matches: {len(matched_results['exact_matches'])}")
print(f"  Fuzzy matches: {len(matched_results['fuzzy_matches'])}")
print(f"  Ambiguous/No matches: {len(matched_results['no_matches'])}")

# Save results
print(f"\n[4/4] Saving results...")

with open('match_results_exact.json', 'w') as f:
    json.dump(matched_results["exact_matches"], f, indent=2)
print(f"  Saved: match_results_exact.json ({len(matched_results['exact_matches'])} entries)")

with open('match_results_fuzzy.json', 'w') as f:
    json.dump(matched_results["fuzzy_matches"], f, indent=2)
print(f"  Saved: match_results_fuzzy.json ({len(matched_results['fuzzy_matches'])} entries)")

with open('match_results_ambiguous.json', 'w') as f:
    json.dump(matched_results["no_matches"], f, indent=2)
print(f"  Saved: match_results_ambiguous.json ({len(matched_results['no_matches'])} entries)")

# Summary
print("\n" + "=" * 120)
print("MATCHING SUMMARY")
print("=" * 120)
total_matched = len(matched_results["exact_matches"]) + len(matched_results["fuzzy_matches"])
total_ambiguous = len(matched_results["no_matches"])
print(f"\nTotal processed: {len(new_companies)}")
print(f"  Auto-resolved (exact + fuzzy): {total_matched} ({total_matched*100/len(new_companies):.1f}%)")
print(f"  Requires manual review: {total_ambiguous} ({total_ambiguous*100/len(new_companies):.1f}%)")

if total_ambiguous > 0:
    print(f"\nAmbiguous entries require manual verification:")
    print(f"  File: match_results_ambiguous.json")
    print(f"  Action: Review and either:")
    print(f"    a) Correct the name if misspelled")
    print(f"    b) Map to the best candidate from SGX")
    print(f"    c) Remove if company is delisted or invalid")

print("\nNext step: Review match_results_ambiguous.json and resolve remaining entries manually.")
print("=" * 120)

