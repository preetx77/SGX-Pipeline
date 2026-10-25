"""
SGX Watchlist Expansion - APPROVED CANDIDATES ONLY
6 new legitimate companies verified against authoritative sources.
Ready for deployment.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# EXPANSION PHASE 1: 6 VERIFIED NEW COMPANIES
# All verified via SGX Official + Yahoo Finance + Investing.com
# All active equities, no duplicates, no delisted entries

EXPANSION_APPROVED = [
    Company(name="DBS GROUP HOLDINGS", code="D05", priority="high", sector="Banking"),
    Company(name="GREAT EASTERN HOLDINGS", code="G07", priority="high", sector="Insurance"),
    Company(name="HAW PAR CORPORATION", code="H02", priority="normal", sector="Consumer"),
    Company(name="JARDINE CYCLE & CARRIAGE", code="C07", priority="normal", sector="Consumer"),
    Company(name="PRUDENTIAL PLC", code="K6S", priority="normal", sector="Insurance"),
    Company(name="VENTURE CORPORATION", code="V03", priority="normal", sector="Tech"),
]

# REJECTED CANDIDATES (44 entries - reasons documented)
EXPANSION_REJECTED = {
    # 34 baseline duplicates - already in production watchlist
    "HQU": "Duplicate - in baseline watchlist",
    "1J5": "Duplicate - in baseline watchlist",
    "L19": "Duplicate - in baseline watchlist",
    "5TP": "Duplicate - in baseline watchlist",
    "G50": "Duplicate - in baseline watchlist",
    "42C": "Duplicate - in baseline watchlist",
    "1V3": "Duplicate - in baseline watchlist",
    "XVG": "Duplicate - in baseline watchlist",
    "VC2": "Duplicate - in baseline watchlist",
    "5AB": "Duplicate - in baseline watchlist",
    "JCO": "Duplicate - in baseline watchlist",
    "U11": "Duplicate - in baseline watchlist",
    "Z74": "Duplicate - in baseline watchlist",
    "S63": "Duplicate - in baseline watchlist",
    "BN4": "Duplicate - in baseline watchlist",
    "G13": "Duplicate - in baseline watchlist",
    "A17U": "Duplicate - in baseline watchlist",
    "C38U": "Duplicate - in baseline watchlist",
    "C8R": "Duplicate - in baseline watchlist",
    "5E2": "Duplicate - in baseline watchlist",
    "9CI": "Duplicate - in baseline watchlist",
    "C09": "Duplicate - in baseline watchlist",
    "F17": "Duplicate - in baseline watchlist",
    "F34": "Duplicate - in baseline watchlist",
    "S68": "Duplicate - in baseline watchlist",
    "S59": "Duplicate - in baseline watchlist",
    "TQ5": "Duplicate - in baseline watchlist",
    "AW9U": "Duplicate - in baseline watchlist",
    "N2IU": "Duplicate - in baseline watchlist",
    "ME8U": "Duplicate - in baseline watchlist",
    "M44U": "Duplicate - in baseline watchlist",
    "O39": "Duplicate - in baseline watchlist",
    "MCOB": "Duplicate - in baseline watchlist",
    "C6L": "Duplicate - in baseline watchlist",
    
    # 2 delisted companies
    "M1Z": "Delisted - not trading",
    "N26": "Delisted - not trading",
    
    # 2 non-equity instruments (bonds)
    "CRC": "Non-equity - bond instrument",
    "AXX": "Non-equity - bond instrument",
    
    # 6 unresolved/incorrect codes
    "OCBC": "Unresolved - use O39 instead (canonical code)",
    "PRU": "Unresolved - use K6S instead (canonical code)",
    "AL8": "Code mismatch - correct code is A13",
    "ENT": "Not found - company not verified",
    "ST": "Code mismatch - correct code is U96",
    "AE8": "Code mismatch - correct code is AWX",
}

if __name__ == "__main__":
    print(f"EXPANSION APPROVED: {len(EXPANSION_APPROVED)} companies")
    for c in EXPANSION_APPROVED:
        print(f"  + {c.code} | {c.name}")
    print(f"\nEXPANSION REJECTED: {len(EXPANSION_REJECTED)} companies")
    print(f"  Reason breakdown:")
    print(f"    - 34 baseline duplicates")
    print(f"    - 2 delisted companies")
    print(f"    - 2 non-equity bonds")
    print(f"    - 6 unresolved/incorrect codes")
