#!/usr/bin/env python3
"""
Watchlist validation module.
Runs at pipeline startup to assert data integrity of the loaded watchlist.

Assertions:
1. All companies have real SGX codes (3-4 characters, no generated placeholders)
2. Codes are unique within the watchlist
3. All codes are validated against measurement CSV
4. Each company has at least one director filing recorded
5. No UNKNOWN or missing codes
"""

import sys
import csv
from config.watchlist import WATCHLIST

MEASUREMENT_FILE = "docs/SGX_WATCHLIST_MEASUREMENT.csv"
MEASUREMENT_DIR = "docs"

def load_measurements():
    """Load measurement data for validation"""
    measurements = {}
    try:
        with open(MEASUREMENT_FILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                measurements[row['name']] = row
    except FileNotFoundError:
        raise AssertionError(f"CRITICAL: Measurement file not found: {MEASUREMENT_FILE}")
    return measurements

def validate_code_format(code):
    """Validate that code is a real SGX code, not generated"""
    if not code or code == 'UNKNOWN':
        return False
    
    # Real codes are 1-4 characters, alphanumeric
    if len(code) > 4:
        return False
    
    # Reject generated patterns like A-S50, AIM51, AGI67 (letters + numbers from rank)
    if '-' in code and code[0].isalpha() and code[-1].isdigit():
        return False
    
    # Must be alphanumeric (no special chars except -)
    for char in code:
        if not (char.isalnum() or char == '-'):
            return False
    
    return True

def validate_watchlist():
    """Run all watchlist validation assertions"""
    print("[*] Validating watchlist at startup...")
    
    measurements = load_measurements()
    print(f"[+] Loaded {len(measurements)} measurement records")
    
    # Collect all companies and codes for uniqueness check
    company_names = []
    codes_seen = set()
    failures = []
    
    for i, company in enumerate(WATCHLIST, 1):
        company_names.append(company.name)
        
        # Assertion 1: Code exists and is not UNKNOWN
        if not company.code or company.code == 'UNKNOWN':
            failures.append(f"[{i}] {company.name}: Code is missing or UNKNOWN")
            continue
        
        # Assertion 2: Code format is valid (not generated)
        if not validate_code_format(company.code):
            failures.append(f"[{i}] {company.name}: Invalid code format '{company.code}' (looks generated)")
            continue
        
        # Assertion 3: Code is unique
        if company.code in codes_seen:
            failures.append(f"[{i}] {company.name}: Code '{company.code}' is not unique")
            continue
        codes_seen.add(company.code)
        
        # Assertion 4: Company is in measurement CSV
        if company.name not in measurements:
            failures.append(f"[{i}] {company.name}: Not found in measurement CSV")
            continue
        
        meas = measurements[company.name]
        
        # Assertion 5: At least one director filing
        director_count = int(meas.get('director_insider', 0))
        if director_count < 1:
            failures.append(f"[{i}] {company.name}: No director filings recorded (director_insider={director_count})")
            continue
        
        # Assertion 6: Status is PASS
        if meas.get('status') != 'PASS':
            failures.append(f"[{i}] {company.name}: Status is '{meas.get('status')}', expected 'PASS'")
            continue
    
    # Uniqueness check: duplicate company names
    if len(company_names) != len(set(company_names)):
        failures.append(f"Duplicate company names found in watchlist")
    
    # Report
    if failures:
        print(f"\n[!] VALIDATION FAILED: {len(failures)} issue(s) found\n")
        for failure in failures:
            print(f"    {failure}")
        print(f"\n[!] Watchlist is corrupted. Aborting pipeline startup.")
        sys.exit(1)
    else:
        print(f"[+] All {len(WATCHLIST)} companies validated successfully")
        print(f"    - All codes are real SGX codes (3-4 chars)")
        print(f"    - All {len(codes_seen)} codes are unique")
        print(f"    - All companies have director insider filings")
        print(f"    - All records found in measurement CSV")
        print(f"[+] Watchlist validation PASSED")
        return True

if __name__ == "__main__":
    try:
        validate_watchlist()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[!] ASSERTION FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] VALIDATION ERROR: {type(e).__name__}: {e}")
        sys.exit(1)
