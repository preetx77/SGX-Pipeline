#!/usr/bin/env python3
"""
Stage 4.5 Results Extraction & Mechanized Gate Decision
Retroactively extracts from preserved logs for the actual Stage 4.5 window:
2026-10-05 13:18:34 to 2026-10-06 13:18:34 UTC

Applies pre-committed branching logic (BRANCH A vs BRANCH B)
"""

from datetime import datetime, timedelta
import sys

print("=" * 120)
print("STAGE 4.5 RESULTS EXTRACTION & GATE DECISION (RETROACTIVE)")
print("=" * 120)

# Define the actual Stage 4.5 window (24 hours starting Oct 5 13:18:34)
stage45_start = datetime(2026, 10, 5, 13, 18, 34)
stage45_end = datetime(2026, 10, 6, 13, 18, 34)

print(f"\n[STAGE 4.5 WINDOW]")
print("-" * 120)
print(f"Start: {stage45_start}")
print(f"End: {stage45_end}")
print(f"Duration: 24 hours")

# Read both log files
all_lines = []
log_files = [
    r'logs/sgx_pipeline.log.1',
    r'logs/sgx_pipeline.log'
]

for log_file in log_files:
    try:
        with open(log_file, 'r', errors='ignore') as f:
            all_lines.extend(f.readlines())
        print(f"Read {log_file}: {sum(1 for _ in open(log_file, 'r', errors='ignore'))} lines")
    except Exception as e:
        print(f"Warning: Could not read {log_file}: {e}")

# Extract timestamps and lines from Stage 4.5 window
all_ts = []
for line in all_lines:
    if ' | ' in line:
        ts_str = line.split(' | ')[0]
        try:
            ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
            all_ts.append((ts, line))
        except:
            pass

if not all_ts:
    print("ERROR: No timestamps found in logs")
    sys.exit(1)

# Filter to Stage 4.5 window only
stage45_lines = [line for ts, line in all_ts if stage45_start <= ts <= stage45_end]

print(f"\nLines in Stage 4.5 window: {len(stage45_lines)}")

if not stage45_lines:
    print(f"ERROR: No logs found in Stage 4.5 window")
    sys.exit(1)

# Extract metrics
dns_count = sum(1 for line in stage45_lines if 'getaddrinfo failed' in line or 'getaddrinfo' in line)
drops_count = sum(1 for line in stage45_lines if 'Resetting dropped connection' in line)
rate_limit_count = sum(1 for line in stage45_lines if '429' in line)
db_error_count = sum(1 for line in stage45_lines if 'database' in line.lower() and 'error' in line.lower())
requests_count = sum(1 for line in stage45_lines if 'GET request to https://' in line)

print(f"\n[RAW METRICS]")
print("-" * 120)
print(f"Total API requests: {requests_count}")
print(f"DNS failures: {dns_count}")
print(f"Connection drops: {drops_count}")
print(f"Rate limit (429) errors: {rate_limit_count}")
print(f"Database errors: {db_error_count}")

# Calculate rates
duration_hours = 24
dns_per_hour = dns_count / duration_hours
drops_per_hour = drops_count / duration_hours
requests_per_hour = requests_count / duration_hours

dns_per_request = dns_count / requests_count if requests_count > 0 else 0
drops_per_request = drops_count / requests_count if requests_count > 0 else 0

print(f"\n[CALCULATED RATES]")
print("-" * 120)
print(f"DNS: {dns_per_hour:.2f}/hour, {dns_per_request:.5f}/request")
print(f"Drops: {drops_per_hour:.2f}/hour, {drops_per_request:.5f}/request")
print(f"Requests: {requests_per_hour:.0f}/hour")
print(f"Rate limits: {rate_limit_count} total")
print(f"DB errors: {db_error_count} total")

# BRANCH DECISION
stage4_p1_request_rate = 275  # Period 1 baseline
tolerance = 0.30
min_req = stage4_p1_request_rate * (1 - tolerance)
max_req = stage4_p1_request_rate * (1 + tolerance)

print(f"\n[BRANCH DECISION LOGIC]")
print("-" * 120)
print(f"Stage 4 Period 1 request rate: {stage4_p1_request_rate}/hour")
print(f"Tolerance: +/-{tolerance*100:.0f}%")
print(f"Acceptable range: {min_req:.0f}-{max_req:.0f} requests/hour")
print(f"Observed rate: {requests_per_hour:.0f} requests/hour")

if min_req <= requests_per_hour <= max_req:
    branch = 'A'
    print(f"\nDECISION: BRANCH A (workload comparable)")
    print(f"Reason: Request rate within tolerance of baseline")
    print(f"Method: Apply errors-per-hour thresholds")
else:
    branch = 'B'
    print(f"\nDECISION: BRANCH B (workload differs)")
    print(f"Reason: Request rate outside +/-30% tolerance")
    print(f"Method: Apply errors-per-request thresholds")

# APPLY GATE CRITERIA
print(f"\n[GATE DECISION - BRANCH {branch}]")
print("-" * 120)

if branch == 'A':
    # Branch A: errors-per-hour thresholds
    dns_pass_threshold = 2.8
    drops_pass_threshold = 0.5
    dns_yellow_upper = 3.5
    drops_yellow_upper = 0.65
    
    print(f"Thresholds (errors/hour):")
    print(f"  PASS: DNS <= {dns_pass_threshold}, Drops <= {drops_pass_threshold}")
    print(f"  YELLOW: DNS {dns_pass_threshold}-{dns_yellow_upper}, Drops {drops_pass_threshold}-{drops_yellow_upper}")
    print(f"  PAUSE: DNS > {dns_yellow_upper} OR Drops > {drops_yellow_upper}")
    print(f"")
    print(f"Observed:")
    print(f"  DNS: {dns_per_hour:.2f}/hour")
    print(f"  Drops: {drops_per_hour:.2f}/hour")
    
    if dns_per_hour <= dns_pass_threshold and drops_per_hour <= drops_pass_threshold:
        decision = "PASS"
    elif dns_per_hour <= dns_yellow_upper and drops_per_hour <= drops_yellow_upper:
        decision = "YELLOW"
    else:
        decision = "PAUSE"

else:  # branch == 'B'
    # Branch B: errors-per-request thresholds
    dns_baseline_per_req = 0.00548
    drops_baseline_per_req = 0.00096
    scaling_factor = 1.5  # 1.5x for 1.25x company scaling
    
    dns_target = dns_baseline_per_req * scaling_factor
    drops_target = drops_baseline_per_req * scaling_factor
    
    dns_pass_threshold = dns_target
    drops_pass_threshold = drops_target
    dns_yellow_upper = dns_target * 1.333
    drops_yellow_upper = drops_target * 1.333
    
    print(f"Thresholds (errors/request):")
    print(f"  PASS: DNS <= {dns_pass_threshold:.5f}, Drops <= {drops_pass_threshold:.5f}")
    print(f"  YELLOW: DNS {dns_pass_threshold:.5f}-{dns_yellow_upper:.5f}, Drops {drops_pass_threshold:.5f}-{drops_yellow_upper:.5f}")
    print(f"  PAUSE: DNS > {dns_yellow_upper:.5f} OR Drops > {drops_yellow_upper:.5f}")
    print(f"")
    print(f"Observed:")
    print(f"  DNS: {dns_per_request:.5f}/request")
    print(f"  Drops: {drops_per_request:.5f}/request")
    
    if dns_per_request <= dns_pass_threshold and drops_per_request <= drops_pass_threshold:
        decision = "PASS"
    elif dns_per_request <= dns_yellow_upper and drops_per_request <= drops_yellow_upper:
        decision = "YELLOW"
    else:
        decision = "PAUSE"

print(f"\n[FINAL DECISION]")
print("-" * 120)
print(f"Gate decision: {decision}")
print(f"")
print(f"Reasoning:")
if branch == 'A':
    if decision == "PASS":
        print(f"  DNS ({dns_per_hour:.2f}/h) and Drops ({drops_per_hour:.2f}/h) both within acceptable limits")
        print(f"  Request rate ({requests_per_hour:.0f}/h) stable compared to baseline")
        print(f"  System scaling linearly - safe to proceed")
    elif decision == "YELLOW":
        print(f"  One or more metrics in YELLOW zone (elevated but not critical)")
        print(f"  Warrants review but does not block continuation")
    else:  # PAUSE
        print(f"  One or more metrics exceed safe thresholds")
        print(f"  Indicates potential scaling issue - investigate before Stage 5")
else:  # branch == 'B'
    if decision == "PASS":
        print(f"  Workload changed significantly (requests/hour != baseline)")
        print(f"  But errors-per-request ({dns_per_request:.5f}/{drops_per_request:.5f}) within limits")
        print(f"  Indicates scaling is stable despite workload change")
    elif decision == "YELLOW":
        print(f"  Workload-normalized errors show caution zone")
    else:  # PAUSE
        print(f"  Workload-normalized errors indicate potential scaling issue")

print("\n" + "=" * 120)
print(f"[EXTRACTION SUMMARY]")
print(f"Extracted from: {len(all_lines)} total log lines across {len(log_files)} files")
print(f"Stage 4.5 window: {stage45_start} to {stage45_end}")
print(f"Matching lines: {len(stage45_lines)}")
print(f"Branch: {branch}")
print(f"Gate decision: {decision}")
print("=" * 120)

