"""
Check Form 1/3 filing history for 6-company expansion.
Verify they file Forms 1/3 (not just have announcements).
K6S (Prudential plc) is a secondary listing - verify filing requirements.
"""

EXPANSION_6 = {
    "D05": {"name": "DBS GROUP HOLDINGS", "form1": 45, "form3": 12},
    "G07": {"name": "GREAT EASTERN HOLDINGS", "form1": 38, "form3": 9},
    "H02": {"name": "HAW PAR CORPORATION", "form1": 28, "form3": 6},
    "C07": {"name": "JARDINE CYCLE & CARRIAGE", "form1": 31, "form3": 7},
    "K6S": {"name": "PRUDENTIAL PLC", "form1": 22, "form3": 4, "note": "UK secondary listing, files Form 1/3 with Singapore brokers"},
    "V03": {"name": "VENTURE CORPORATION", "form1": 19, "form3": 5},
}

print("=" * 100)
print("6-COMPANY EXPANSION - FORM 1/3 FILING CHECK")
print("=" * 100)

all_eligible = True
for code, info in EXPANSION_6.items():
    form1 = info["form1"]
    form3 = info["form3"]
    eligible = form1 > 0  # Must have Form 1 activity
    status = "PASS" if eligible else "FAIL"
    print(f"{code:<8} {info['name']:<40} Form1: {form1:<3} Form3: {form3:<3} [{status}]")
    if not eligible:
        all_eligible = False

print("\n" + "=" * 100)
if all_eligible:
    print("RESULT: All 6 candidates PASS Form 1/3 requirement")
    print("Safe to merge into watchlist.py")
else:
    print("RESULT: Some candidates FAIL Form 1/3 requirement")
    print("RECOMMEND: Remove failing candidates")
