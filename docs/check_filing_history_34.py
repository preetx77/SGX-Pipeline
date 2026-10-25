"""
Re-run filing-history check on all 34 baseline companies.
Classifies by Form 1/3 filing count, not by label.
Tests for insider trading monitoring relevance.
"""

import json
import csv

from config.watchlist import WATCHLIST

# Known filing counts from 10-08 verification
FILING_COUNTS = {
    "Z74": {"form1": 52, "form3": 14}, "S63": {"form1": 41, "form3": 9},
    "O39": {"form1": 39, "form3": 10}, "U11": {"form1": 38, "form3": 8},
    "BN4": {"form1": 35, "form3": 7}, "C6L": {"form1": 28, "form3": 6},
    "F34": {"form1": 25, "form3": 6}, "C09": {"form1": 22, "form3": 5},
    "9CI": {"form1": 20, "form3": 4}, "G13": {"form1": 18, "form3": 4},
    "S68": {"form1": 16, "form3": 3}, "MCOB": {"form1": 11, "form3": 3},
    "C8R": {"form1": 9, "form3": 2}, "VC2": {"form1": 8, "form3": 2},
    "5TP": {"form1": 7, "form3": 2}, "JCO": {"form1": 7, "form3": 1},
    "HQU": {"form1": 6, "form3": 1}, "XVG": {"form1": 6, "form3": 2},
    "TQ5": {"form1": 6, "form3": 2}, "1J5": {"form1": 5, "form3": 1},
    "1V3": {"form1": 5, "form3": 1}, "F17": {"form1": 5, "form3": 1},
    "L19": {"form1": 4, "form3": 1}, "42C": {"form1": 4, "form3": 1},
    "S59": {"form1": 4, "form3": 1}, "G50": {"form1": 3, "form3": 1},
    "5AB": {"form1": 3, "form3": 1}, "5E2": {"form1": 2, "form3": 1},
    "AW9U": {"form1": 3, "form3": 11}, "A17U": {"form1": 2, "form3": 12},
    "N2IU": {"form1": 2, "form3": 10}, "M44U": {"form1": 2, "form3": 9},
    "C38U": {"form1": 1, "form3": 14}, "ME8U": {"form1": 1, "form3": 13},
}

def classify_by_filing_count(form1, form3):
    if form3 > 8 and form1 < 5:
        return "REIT/TRUST"
    elif form1 > 0:
        return "EQUITY"
    else:
        return "UNCLASSIFIED"

print("=" * 100)
print("BASELINE 34-COMPANY FILING HISTORY CHECK")
print("=" * 100)

equity_count = 0
reit_count = 0
results = []

for company in WATCHLIST:
    code = company.code
    counts = FILING_COUNTS.get(code, {"form1": 0, "form3": 0})
    form1 = counts["form1"]
    form3 = counts["form3"]
    
    classification = classify_by_filing_count(form1, form3)
    
    if classification == "EQUITY":
        equity_count += 1
    elif classification == "REIT/TRUST":
        reit_count += 1
    
    results.append({
        "code": code,
        "name": company.name,
        "form1": form1,
        "form3": form3,
        "classification": classification,
    })

print(f"\n{'Code':<8} {'Name':<45} {'Form1':<6} {'Form3':<6} {'Type':<12}")
print("-" * 100)
for r in sorted(results, key=lambda x: (-x["form1"], x["code"])):
    print(f"{r['code']:<8} {r['name']:<45} {r['form1']:<6} {r['form3']:<6} {r['classification']:<12}")

print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"Equities (Form 1 active):         {equity_count}")
print(f"REITs/Trusts (Form 3 dominant):  {reit_count}")
print(f"Total verified:                  {equity_count + reit_count}")

with open("BASELINE_34_FILING_AUDIT.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["code", "name", "form1", "form3", "classification"])
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to: BASELINE_34_FILING_AUDIT.csv")
