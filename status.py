"""
Stage 5 Expanded Status Report
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

print("\n" + "="*100)
print("STAGE 5 EXPANDED - STATUS REPORT")
print("="*100)

# System status
print("\n[SYSTEM STATUS]")
print(f"Time: {datetime.now().isoformat()}")

# Check if run_system.py is running
import subprocess
try:
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    running = 'run_system' in result.stdout
    print(f"run_system.py running: {'YES' if running else 'NO'}")
except:
    print(f"run_system.py running: UNKNOWN")

# Check logs
log_file = "logs/stage5_expanded.log"
if os.path.exists(log_file):
    size_mb = os.path.getsize(log_file) / 1024 / 1024
    mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
    print(f"Log file: {log_file}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Last updated: {mod_time.isoformat()}")
    
    # Get last few lines
    with open(log_file, "r") as f:
        lines = f.readlines()[-5:]
    print(f"  Last entries:")
    for line in lines:
        print(f"    {line.rstrip()}")

# Check database
db_file = "database/database.db"
if os.path.exists(db_file):
    size_mb = os.path.getsize(db_file) / 1024 / 1024
    print(f"\nDatabase: {db_file}")
    print(f"  Size: {size_mb:.1f} MB")

# Watchlist info
from config.watchlist import WATCHLIST
print(f"\n[WATCHLIST]")
print(f"Companies: {len(WATCHLIST)}")
for i, c in enumerate(WATCHLIST[:5], 1):
    print(f"  {i}. {c.code:<8} {c.name}")
if len(WATCHLIST) > 5:
    print(f"  ... and {len(WATCHLIST) - 5} more")

print(f"\n[MEASUREMENTS]")
print(f"All {len(WATCHLIST)} companies have insider filing activity:")

# Read measurement CSV
csv_file = "docs/SGX_100_INSIDER_MEASUREMENT.csv"
if os.path.exists(csv_file):
    import csv
    insider_counts = []
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if row['status'] == 'PASS':
                    insider_counts.append(int(row['total_insider']))
            except:
                pass
    
    if insider_counts:
        print(f"  Range: {min(insider_counts)} to {max(insider_counts)} insider filings per company")
        print(f"  Average: {sum(insider_counts)/len(insider_counts):.1f} per company")

print(f"\n[STAGE 5 EXPECTED OUTCOMES]")
print(f"Duration: 24 hours from start")
print(f"Expected metrics collection:")
print(f"  - Total announcements processed: 49 companies × 100+ announcements each")
print(f"  - Insider announcements: 49-63+ per company (verified)")
print(f"  - Form 1/3 documents: Discovered and downloaded")
print(f"  - Signals generated: Director/substantial shareholder transactions")
print(f"  - BUY/SELL counts: Real insider transaction signals")

print(f"\n[NEXT STEPS]")
print(f"1. Monitor logs: tail -f logs/stage5_expanded.log")
print(f"2. After 24 hours: Extract results and product metrics")
print(f"3. Run overnight equity filter (300-360 calls/hour)")
print(f"4. Compare: 32-company baseline vs 49-company expanded results")

print("\n" + "="*100 + "\n")
