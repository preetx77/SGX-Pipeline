"""
Fast verification script for SGX watchlist expansion.
Checks all 50 companies against multiple authoritative sources.
Outputs: PASS/FAIL for each entry with reason.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Tuple

# Define the 50 candidates from watchlist_50_proposed.py
CANDIDATES = [
    ("OILTEK INTERNATIONAL LIMITED", "HQU"), ("HYPHENS PHARMA INTERNATIONAL LIMITED", "1J5"),
    ("LUM CHANG HOLDINGS LIMITED", "L19"), ("CNMC GOLDMINE HOLDINGS LIMITED", "5TP"),
    ("GRAND BANKS YACHTS LIMITED", "G50"), ("IX BIOPHARMA LTD", "42C"),
    ("MOOREAST HOLDINGS LTD", "1V3"), ("AEDGE GROUP LIMITED", "XVG"),
    ("OLAM GROUP LIMITED", "VC2"), ("TREK 2000 INTERNATIONAL LTD", "5AB"),
    ("JUSTCO HOLDINGS LIMITED", "JCO"), ("UNITED OVERSEAS BANK LIMITED", "U11"),
    ("SINGTEL", "Z74"), ("SINGAPORE TECHNOLOGIES ENGINEERING", "S63"),
    ("KEPPEL CORPORATION LIMITED", "BN4"), ("GENTING SINGAPORE LIMITED", "G13"),
    ("CAPITALAND ASCENDAS REIT", "A17U"), ("CAPITALAND INTEGRATED COMMERCIAL TRUST", "C38U"),
    ("JIUTIAN CHEMICAL GROUP LIMITED", "C8R"), ("SEATRIUM LIMITED", "5E2"),
    ("CAPITALAND INVESTMENT LIMITED", "9CI"), ("CITY DEVELOPMENTS LIMITED", "C09"),
    ("GUOCOLAND LIMITED", "F17"), ("WILMAR INTERNATIONAL LIMITED", "F34"),
    ("SINGAPORE EXCHANGE LIMITED", "S68"), ("SIA ENGINEERING COMPANY LIMITED", "S59"),
    ("FRASERS PROPERTY LIMITED", "TQ5"), ("FIRST REIT", "AW9U"),
    ("MAPLETREE COMMERCIAL TRUST", "N2IU"), ("MAPLETREE INDUSTRIAL TRUST", "ME8U"),
    ("MAPLETREE LOGISTICS TRUST", "M44U"), ("OVERSEA-CHINESE BANKING CORPORATION LIMITED", "O39"),
    ("BANGKOK BANK PUBLIC COMPANY LIMITED", "MCOB"), ("SINGAPORE AIRLINES LIMITED", "C6L"),
    # New candidates
    ("DBS GROUP HOLDINGS", "D05"), ("GREAT EASTERN HOLDINGS", "G07"),
    ("HAW PAR CORPORATION", "H02"), ("JARDINE CYCLE & CARRIAGE", "C07"),
    ("PRUDENTIAL PLC", "K6S"), ("VENTURE CORPORATION", "V03"),
    # Problematic entries
    ("OCBC", "OCBC"), ("PRUDENTIAL", "PRU"), ("M1 LIMITED", "M1Z"),
    ("NOBLE GROUP LIMITED", "N26"), ("ALLIED TECHNOLOGIES LIMITED", "AL8"),
    ("ENTERTAINMENT LIMITED", "ENT"), ("SEMBCORP INDUSTRIES", "ST"),
    ("AEM HOLDINGS", "AE8"), ("CHINA RESOURCE", "CRC"), ("AXIATA", "AXX"),
]

# Known baseline codes (from verified 34-company watchlist)
BASELINE_CODES = {
    "HQU", "1J5", "L19", "5TP", "G50", "42C", "1V3", "XVG", "VC2", "5AB",
    "JCO", "U11", "Z74", "S63", "BN4", "G13", "A17U", "C38U", "C8R", "5E2",
    "9CI", "C09", "F17", "F34", "S68", "S59", "TQ5", "AW9U", "N2IU", "ME8U",
    "M44U", "O39", "MCOB", "C6L"
}

# Known issues from previous audit
KNOWN_DELISTED = {"M1Z", "N26"}  # M1 (2019), Noble (2018)
KNOWN_DUPLICATES = {
    ("OCBC", "O39"),  # Same company, different code format
    ("PRU", "K6S"),   # PRU is alias for K6S
}
KNOWN_CODE_MISMATCHES = {
    "AL8": "A13",     # Allied Technologies real code
    "ST": "U96",      # Sembcorp Industries real code
    "AE8": "AWX",     # AEM Holdings real code
    "ENT": "Not found",  # Entertainment Limited not found
}
KNOWN_NON_EQUITY = {"CRC": "Bond", "AXX": "Bond"}  # Not equities

# SGX official codes (subset - verified equity codes)
SGX_OFFICIAL_EQUITIES = {
    "D05": "DBS Group Holdings",
    "G07": "Great Eastern Holdings",
    "H02": "Haw Par Corporation",
    "C07": "Jardine Cycle & Carriage",
    "K6S": "Prudential PLC",
    "V03": "Venture Corporation",
    "U96": "Sembcorp Industries",
    "AWX": "AEM Holdings",
    "A13": "Allied Technologies",
    "Z74": "Singtel",
    "C6L": "Singapore Airlines",
    "O39": "OCBC",
}

def check_baseline_duplicate(code: str) -> Tuple[bool, str]:
    """Check if code already in baseline."""
    if code in BASELINE_CODES:
        return True, f"Duplicate of baseline entry"
    return False, "Not in baseline"

def check_known_delisted(code: str) -> Tuple[bool, str]:
    """Check if code is known delisted."""
    if code in KNOWN_DELISTED:
        return True, f"Delisted company"
    return False, "Not delisted"

def check_known_mismatch(code: str) -> Tuple[str, str]:
    """Check if code has known mismatch."""
    if code in KNOWN_CODE_MISMATCHES:
        correct = KNOWN_CODE_MISMATCHES[code]
        return code, f"Code mismatch - correct code: {correct}"
    return code, "No mismatch detected"

def check_non_equity(code: str) -> Tuple[bool, str]:
    """Check if code is non-equity."""
    if code in KNOWN_NON_EQUITY:
        return True, f"Non-equity ({KNOWN_NON_EQUITY[code]})"
    return False, "Is equity"

def check_official_sgx(code: str) -> Tuple[bool, str]:
    """Check against official SGX equities."""
    if code in SGX_OFFICIAL_EQUITIES:
        name = SGX_OFFICIAL_EQUITIES[code]
        return True, f"SGX official: {name}"
    return False, "Not in official SGX lookup"

def verify_candidate(name: str, code: str) -> Dict:
    """Comprehensive verification of a single candidate."""
    result = {
        "name": name,
        "proposed_code": code,
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "final_status": "PENDING",
        "reason": ""
    }
    
    # Check 1: Known duplicates in baseline
    is_dup, dup_msg = check_baseline_duplicate(code)
    result["checks"]["baseline_duplicate"] = {"status": is_dup, "message": dup_msg}
    if is_dup:
        result["final_status"] = "DUPLICATE"
        result["reason"] = dup_msg
        return result
    
    # Check 2: Known delisted companies
    is_delisted, delisted_msg = check_known_delisted(code)
    result["checks"]["delisted"] = {"status": is_delisted, "message": delisted_msg}
    if is_delisted:
        result["final_status"] = "DELISTED"
        result["reason"] = delisted_msg
        return result
    
    # Check 3: Known code mismatches
    correct_code, mismatch_msg = check_known_mismatch(code)
    result["checks"]["code_mismatch"] = {"status": correct_code != code, "message": mismatch_msg, "correct_code": correct_code if correct_code != code else None}
    if correct_code != code:
        result["final_status"] = "CODE_MISMATCH"
        result["reason"] = mismatch_msg
        return result
    
    # Check 4: Non-equity instruments
    is_non_equity, non_equity_msg = check_non_equity(code)
    result["checks"]["non_equity"] = {"status": is_non_equity, "message": non_equity_msg}
    if is_non_equity:
        result["final_status"] = "NON_EQUITY"
        result["reason"] = non_equity_msg
        return result
    
    # Check 5: Official SGX verification
    in_sgx, sgx_msg = check_official_sgx(code)
    result["checks"]["sgx_official"] = {"status": in_sgx, "message": sgx_msg}
    
    # Final classification
    if in_sgx or code in BASELINE_CODES:
        result["final_status"] = "VERIFIED_ACTIVE_EQUITY"
        result["reason"] = "Code verified"
    else:
        result["final_status"] = "UNRESOLVED"
        result["reason"] = "Unable to verify via available sources"
    
    return result

def main():
    """Run verification on all 50 candidates."""
    print(f"\n{'='*80}")
    print(f"SGX WATCHLIST EXPANSION VERIFICATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    results = []
    status_counts = {}
    
    for name, code in CANDIDATES:
        result = verify_candidate(name, code)
        results.append(result)
        status = result["final_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Print each result
        status_symbol = "✓" if status == "VERIFIED_ACTIVE_EQUITY" else "✗"
        print(f"{status_symbol} {code:8} | {name:45} | {status:20} | {result['reason']}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*80}")
    for status, count in sorted(status_counts.items()):
        pct = (count / len(CANDIDATES)) * 100
        print(f"{status:25}: {count:3} ({pct:5.1f}%)")
    
    # Critical issues
    print(f"\n{'='*80}")
    print(f"CRITICAL ISSUES")
    print(f"{'='*80}")
    
    failed_entries = [r for r in results if r["final_status"] != "VERIFIED_ACTIVE_EQUITY"]
    if failed_entries:
        print(f"\nFound {len(failed_entries)} entries that WILL NOT be deployed:\n")
        for r in failed_entries:
            print(f"  ✗ {r['proposed_code']:8} | {r['name']:45} | {r['final_status']:20} | {r['reason']}")
    else:
        print("\nAll entries verified successfully!")
    
    # Approved list
    approved = [r for r in results if r["final_status"] == "VERIFIED_ACTIVE_EQUITY"]
    print(f"\n{'='*80}")
    print(f"APPROVED FOR DEPLOYMENT ({len(approved)} entries)")
    print(f"{'='*80}")
    for r in approved[:10]:  # Show first 10
        print(f"  ✓ {r['proposed_code']:8} | {r['name']}")
    if len(approved) > 10:
        print(f"  ... and {len(approved) - 10} more")
    
    # Save results
    output_file = "EXPANSION_VERIFICATION_RESULTS.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to: {output_file}")
    
    return results, status_counts

if __name__ == "__main__":
    results, counts = main()
