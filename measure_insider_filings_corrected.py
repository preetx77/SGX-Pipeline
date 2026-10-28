"""
Corrected insider filing measurement.
- Uses iter_company_announcements for full pagination
- Handles name mismatches by fetching issuer names from /companylist
- Marks total=0 as UNMEASURED (not FAIL)
- Counts Director/CEO vs Substantial Shareholder separately
"""

import time
import csv
from datetime import datetime, timedelta
from config.watchlist import WATCHLIST
from scraper.client import SGXClient
from pipeline.announcement_router import AnnouncementRouter

# 24-month lookback window
end_date = datetime.now()
start_date = end_date - timedelta(days=730)

period_start = start_date.strftime("%Y%m%d_000000")
period_end = end_date.strftime("%Y%m%d_235959")

print(f"\n{'='*130}")
print(f"CORRECTED INSIDER FILING MEASUREMENT - {len(WATCHLIST)} Companies")
print(f"{'='*130}")
print(f"Window: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (24 months)")
print(f"Method: iter_company_announcements (full pagination)")
print(f"\n{'Code':<8} {'Name':<40} {'Total':<8} {'Director':<10} {'Shareholder':<12} {'Total':<8} Status")
print("-" * 130)

client = SGXClient()
router = AnnouncementRouter()

# Fetch issuer list for name lookups
print("Fetching issuer list...", end="", flush=True)
try:
    company_list = client.get_company_list()
    issuer_map = {}
    if company_list and 'data' in company_list:
        for entry in company_list['data']:
            if isinstance(entry, dict):
                code = entry.get('code') or entry.get('stock_code')
                name = entry.get('name') or entry.get('company_name')
                if code and name:
                    issuer_map[code] = name
    print(f" {len(issuer_map)} issuers")
except Exception as e:
    print(f" FAILED: {e}")
    issuer_map = {}

results = []

for i, company in enumerate(WATCHLIST, 1):
    code = company.code
    name = company.name
    
    # Try provided name first, fall back to issuer_map for known mismatches
    query_name = name
    name_source = "watchlist"
    
    # Check if this code has a different issuer name
    if code in issuer_map and issuer_map[code] != name:
        query_name = issuer_map[code]
        name_source = "issuer_map"
    
    try:
        # Iterate through ALL announcements (paginated)
        all_anns = []
        director_anns = []
        shareholder_anns = []
        
        for ann in client.iter_company_announcements(
            query_name,
            period_start=period_start,
            period_end=period_end,
            page_size=100
        ):
            all_anns.append(ann)
            
            # Categorize by type
            if router.is_insider(ann):
                # Further classify
                category = (ann.category or "").lower()
                if "director" in category or "ceo" in category:
                    director_anns.append(ann)
                elif "substantial" in category or "unitholder" in category:
                    shareholder_anns.append(ann)
                else:
                    # Fallback to director if unclear
                    director_anns.append(ann)
        
        total = len(all_anns)
        director_count = len(director_anns)
        shareholder_count = len(shareholder_anns)
        insider_count = director_count + shareholder_count
        
        # Determine status
        if total == 0:
            status = "UNMEASURED"
            status_sym = "?"
        elif insider_count > 0:
            status = "PASS"
            status_sym = "✓"
        else:
            status = "FAIL"
            status_sym = "✗"
        
        name_marker = f" [{name_source}]" if name_source == "issuer_map" else ""
        print(f"{status_sym} {code:<8} {name:<40} {total:<8} {director_count:<10} {shareholder_count:<12} {insider_count:<8} {status}{name_marker}")
        
        results.append({
            "code": code,
            "watchlist_name": name,
            "query_name": query_name,
            "name_source": name_source,
            "window_start": start_date.isoformat(),
            "window_end": end_date.isoformat(),
            "total_announcements": total,
            "director_insider_count": director_count,
            "shareholder_insider_count": shareholder_count,
            "total_insider_count": insider_count,
            "measurement_status": status,
            "measurement_time": datetime.now().isoformat()
        })
        
        time.sleep(1)
    
    except Exception as e:
        error_msg = str(e)[:80]
        print(f"✗ {code:<8} {name:<40} ERROR: {error_msg}")
        results.append({
            "code": code,
            "watchlist_name": name,
            "query_name": query_name,
            "name_source": name_source,
            "window_start": start_date.isoformat(),
            "window_end": end_date.isoformat(),
            "total_announcements": "ERROR",
            "director_insider_count": "ERROR",
            "shareholder_insider_count": "ERROR",
            "total_insider_count": "ERROR",
            "measurement_status": "ERROR",
            "measurement_time": datetime.now().isoformat()
        })
        time.sleep(1)

# Summary
print(f"\n{'='*130}")
print(f"SUMMARY")
print(f"{'='*130}")

pass_list = [r for r in results if r.get("measurement_status") == "PASS"]
fail_list = [r for r in results if r.get("measurement_status") == "FAIL"]
unmeasured_list = [r for r in results if r.get("measurement_status") == "UNMEASURED"]
error_list = [r for r in results if r.get("measurement_status") == "ERROR"]

print(f"PASS (has insider filings):     {len(pass_list)}")
print(f"FAIL (zero insider, full scan): {len(fail_list)}")
print(f"UNMEASURED (zero total anns):   {len(unmeasured_list)}")
print(f"ERROR (query failed):           {len(error_list)}")

if fail_list:
    print(f"\nFAIL - Valid zeros (confirmed via full scan, safe to drop):")
    for r in fail_list:
        print(f"  {r['code']:<8} {r['watchlist_name']:<40} total={r['total_announcements']}")

if unmeasured_list:
    print(f"\nUNMEASURED - Zero announcements returned (name mismatch likely, restore to watchlist):")
    for r in unmeasured_list:
        source_note = f" (retried as: {r['query_name']})" if r['query_name'] != r['watchlist_name'] else ""
        print(f"  {r['code']:<8} {r['watchlist_name']:<40}{source_note}")

if error_list:
    print(f"\nERROR - Query failed:")
    for r in error_list[:5]:
        print(f"  {r['code']:<8} {r['watchlist_name']:<40}")

# Save CSV
output_file = "docs/INSIDER_FILINGS_MEASUREMENT_CORRECTED.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["code", "watchlist_name", "query_name", "name_source", "window_start", "window_end", 
                  "total_announcements", "director_insider_count", "shareholder_insider_count", 
                  "total_insider_count", "measurement_status", "measurement_time"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"\nResults saved to: {output_file}")
