"""
Measure insider filing activity for all 40 watchlist companies.
Uses the pipeline's own definition of insider announcements.
"""

import time
import csv
from datetime import datetime, timedelta
from config.watchlist import WATCHLIST
from scraper.client import SGXClient
from pipeline.announcement_router import AnnouncementRouter

# 24-month lookback window (same as announcement_service.py)
end_date = datetime.now()
start_date = end_date - timedelta(days=730)

print(f"\n{'='*120}")
print(f"INSIDER FILING MEASUREMENT - {len(WATCHLIST)} Companies")
print(f"{'='*120}")
print(f"Window: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (24 months)")
print(f"Definition: AnnouncementRouter.is_insider() keywords")
print(f"  - 'disclosure of interest'")
print(f"  - 'change in interest'")
print(f"  - 'director's interest'")
print(f"  - 'substantial shareholder'")
print(f"\n{'Code':<8} {'Name':<45} {'Total':<8} {'Insider':<8} {'Rate':<8} Sample Titles")
print("-" * 120)

client = SGXClient()
router = AnnouncementRouter()
results = []

for i, company in enumerate(WATCHLIST, 1):
    code = company.code
    name = company.name
    
    period_start = start_date.strftime("%Y%m%d_000000")
    period_end = end_date.strftime("%Y%m%d_235959")
    
    try:
        announcements = client.get_company_announcement(
            name,
            period_start=period_start,
            period_end=period_end
        )
    except Exception as e:
        print(f"✗ {code:<8} {name:<45} ERROR: {e}")
        results.append({
            "code": code,
            "name": name,
            "window_start": start_date.isoformat(),
            "window_end": end_date.isoformat(),
            "total_announcements": "ERROR",
            "insider_count": "ERROR",
            "insider_rate": "ERROR",
            "sample_titles": str(e),
            "measurement_time": datetime.now().isoformat()
        })
        time.sleep(1)
        continue
    
    # Filter by insider definition
    insider_anns = [a for a in announcements if router.is_insider(a)]
    
    total = len(announcements)
    insider = len(insider_anns)
    rate = f"{(insider/total*100):.1f}%" if total > 0 else "N/A"
    
    # Get sample titles (first 3)
    sample_titles = [a.title for a in insider_anns[:3]]
    samples_str = " | ".join(sample_titles[:2]) if sample_titles else "(none)"
    
    status = "✓" if insider > 0 else "✗"
    print(f"{status} {code:<8} {name:<45} {total:<8} {insider:<8} {rate:<8} {samples_str}")
    
    results.append({
        "code": code,
        "name": name,
        "window_start": start_date.isoformat(),
        "window_end": end_date.isoformat(),
        "total_announcements": total,
        "insider_count": insider,
        "insider_rate": rate,
        "sample_title_1": sample_titles[0] if len(sample_titles) > 0 else "",
        "sample_title_2": sample_titles[1] if len(sample_titles) > 1 else "",
        "sample_title_3": sample_titles[2] if len(sample_titles) > 2 else "",
        "measurement_time": datetime.now().isoformat()
    })
    
    time.sleep(1)

# Summary
print(f"\n{'='*120}")
print(f"SUMMARY")
print(f"{'='*120}")

passed = [r for r in results if r.get("insider_count", 0) > 0]
failed = [r for r in results if r.get("insider_count", 0) == 0]
errors = [r for r in results if r.get("insider_count") == "ERROR"]

print(f"Companies with insider filings:   {len(passed)}/{len(WATCHLIST)}")
print(f"Companies with NO insider filings: {len(failed)}")
print(f"Query errors:                     {len(errors)}")

if failed:
    print(f"\nCOMPANIES WITH ZERO INSIDER ANNOUNCEMENTS (will be dropped):")
    for r in failed:
        print(f"  - {r['code']:<8} {r['name']}")

if errors:
    print(f"\nQUERY ERRORS:")
    for r in errors:
        print(f"  - {r['code']:<8} {r['name']:<45} {r['sample_titles']}")

# Save CSV
output_file = "docs/INSIDER_FILINGS_MEASUREMENT.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["code", "name", "window_start", "window_end", "total_announcements", 
                  "insider_count", "insider_rate", "sample_title_1", "sample_title_2", 
                  "sample_title_3", "measurement_time"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"\nResults saved to: {output_file}")
print(f"Recommendation: Drop {len(failed)} companies with zero insider filings")
print(f"Verified watchlist: {len(passed)}/{len(WATCHLIST)} companies")
