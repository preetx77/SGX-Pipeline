#!/usr/bin/env python3
"""
Stage 4.5 Results Extraction & Mechanized Gate Decision
Applies pre-committed branching logic (BRANCH A vs BRANCH B)
Run this at the 24-hour mark after Stage 4.5 launch
"""

from datetime import datetime, timedelta
import sys

print("=" * 120)
print("STAGE 4.5 RESULTS EXTRACTION & GATE DECISION")
print("=" * 120)

# Read logs
try:
    with open('logs/sgx_pipeline.log', 'r', errors='ignore') as f:
        lines = f.readlines()
except Exception as e:
    print(f"ERROR reading logs: {e}")
    sys.exit(1)

# Get timestamps for Stage 4.5 window
# Stage 4.5 started at 2026-10-03 00:00:00 UTC
# Extract 24-hour window ending at that time + 24h
all_ts = []
for line in lines:
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

# Find Stage 4.5 window (approximate: look for lines AFTER 2026-10-03 00:00)
cutoff_start = datetime(2026, 10, 3, 0, 0, 0)
cutoff_end = cutoff_start + timedelta(hours=24)

stage45_lines = [line for ts, line in all_ts if cutoff_start <= ts <= cutoff_end]

if not stage45_lines:
    print(f"WARNING: No logs found in Stage 4.5 window ({cutoff_start} to {cutoff_end})")
    print("This may mean Stage 4.5 hasn't launched yet, or the time window is wrong")
    sys.exit(1)

print(f"\n[STAGE 4.5 WINDOW]")
print("-" * 120)
print(f"Start: {cutoff_start}")
print(f"End: {cutoff_end}")
print(f"Lines extracted: {len(stage45_lines)}")

# Extract metrics
dns_count = sum(1 for line in stage45_lines if 'getaddrinfo failed' in line)
drops_count = sum(1 for line in stage45_lines if 'Resetting dropped connection' in line)
requests_count = sum(1 for line in stage45_lines if 'GET request to https://' in line)

print(f"\n[RAW METRICS]")
print("-" * 120)
print(f"DNS failures: {dns_count}")
print(f"Connection drops: {drops_count}")
print(f"API requests: {requests_count}")

# Calculate rates
dns_per_hour = dns_count / 24
drops_per_hour = drops_count / 24
requests_per_hour = requests_count / 24

dns_per_request = dns_count / requests_count if requests_count > 0 else 0
drops_per_request = drops_count / requests_count if requests_count > 0 else 0

print(f"\n[CALCULATED RATES]")
print("-" * 120)
print(f"DNS: {dns_per_hour:.2f}/hour, {dns_per_request:.5f}/request")
print(f"Drops: {drops_per_hour:.2f}/hour, {drops_per_request:.5f}/request")
print(f"Requests: {requests_per_hour:.0f}/hour")

# BRANCH DECISION
stage4_p1_request_rate = 275  # Period 1 baseline
tolerance = 0.30
min_req = stage4_p1_request_rate * (1 - tolerance)
max_req = stage4_p1_request_rate * (1 + tolerance)

print(f"\n[BRANCH DECISION LOGIC]")
print("-" * 120)
print(f"Stage 4 Period 1 request rate: {stage4_p1_request_rate}/hour")
print(f"Tolerance: ±{tolerance*100:.0f}%")
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
    print(f"Reason: Request rate outside ±30% tolerance")
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
    print(f"  PASS: DNS ≤ {dns_pass_threshold}, Drops ≤ {drops_pass_threshold}")
    print(f"  YELLOW: DNS 2.8-{dns_yellow_upper}, Drops 0.5-{drops_yellow_upper}")
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
    print(f"  PASS: DNS ≤ {dns_pass_threshold:.5f}, Drops ≤ {drops_pass_threshold:.5f}")
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
