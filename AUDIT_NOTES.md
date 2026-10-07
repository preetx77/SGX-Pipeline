# Database Concurrency Fix - Audit Trail

## Problem Statement
Stage 3 fresh-start (50 companies) failed with `sqlite3.ProgrammingError: Cannot operate on a closed database.` when MarketIngestor and SGXWatcher threads ran concurrently.

## Root Cause Analysis

### Incorrect Theories (Investigated and Rejected)
1. **Singleton Pattern**: Initially thought multiple `DatabaseManager` instances per thread was the issue. Implemented singleton connection sharing across threads.
   - Result: Introduced **"Recursive use of cursors not allowed"** error
   - Reason: SQLite cursors cannot be safely shared across threads even with `check_same_thread=False`. Concurrency requires separate connections per thread.

2. **Missing Thread Safety Lock**: Added `threading.Lock()` around all database operations in DatabaseManager
   - Result: Same cursor recursion error (lock prevented concurrent access but didn't solve cursor state corruption)
   - Reason: Lock around cursor operations doesn't fix SQLite's single-threaded cursor design

3. **Dependency Injection Refactor**: Attempted to pass single shared DatabaseManager instance through entire service layer (MarketIngestor → AnnouncementService → All Repositories)
   - Result: Incomplete refactoring, didn't reach all dependency chains (e.g., InsiderPipeline creating its own repositories)
   - Abandoned: Too invasive, didn't solve the core issue

### Actual Root Cause
**Lifecycle bug in `run_system.py` cleanup function**: The `cleanup()` function, registered with `atexit`, was calling `.close()` on repositories while the threads were still running and potentially holding database connections. This caused:
- Thread A in middle of a database query
- Cleanup handler fires (on any exception or signal)
- Calls `ingestor.close()` → `service.close()` → `repository.close()` → `DatabaseManager.close()`
- Connection closes while Thread B is trying to execute a query → "Cannot operate on a closed database"

## Solution Implemented

**Minimal, targeted fix**: Remove premature `.close()` calls from `run_system.py` cleanup function.

**Rationale**:
- Each repository already creates its own `DatabaseManager` instance (separate connections per thread)
- Multiple SQLite connections to the same file IS supported and safe (WAL mode + timeout=10.0 handles write serialization)
- Connections don't need to be explicitly closed during runtime - OS will close file handles on process exit
- This avoids the singleton/cursor-sharing problem entirely by keeping connections independent

**Code change**: `run_system.py` cleanup() function now:
- Does NOT call `ingestor.close()`
- Does NOT call `watcher.repo.close()`
- Lets process exit naturally, OS handles file cleanup

## Test Results
- 2+ minutes concurrent operation: ✓ No "recursive cursor" errors
- 2+ minutes concurrent operation: ✓ No "Cannot operate on closed database" errors
- Errors present: DNS failures (external), not database lifecycle issues

## Architecture After Fix
- MarketIngestor creates AnnouncementRepository → creates DatabaseManager → creates connection
- SGXWatcher creates AnnouncementRepository → creates DatabaseManager → creates connection
- Two separate connections to same SQLite database file
- WAL mode prevents corruption
- 10s timeout on locks allows retry when writes overlap
- No shared connection, no cross-thread cursor access, no premature closing

## Lessons Learned
1. SQLite connections ARE thread-safe for multiple connections, but cursors are NOT thread-safe when shared
2. Don't add abstractions (singleton, lock) to fix lifecycle bugs - fix the lifecycle bug
3. Test under actual concurrent load for 10+ minutes, not just immediate startup
4. The simplest solution that doesn't require complex refactoring is often correct

## Files Modified
- `run_system.py`: Removed `.close()` calls from cleanup() function

## Date
2026-09-11 00:26:29 to 2026-09-11 00:xx:xx (Database fix investigation)


========================================================================================================================
STAGE 4.5 PREPARATION - 2026-09-19 08:05:18
========================================================================================================================


========================================================================================================================
STAGE 4.5 DELAYED LAUNCH - 2026-09-19 08:09:14 UTC
========================================================================================================================
Scheduled launch: 2026-09-20 00:00:00 UTC
Time until launch: 15.8 hours
Reason for delay: Clock-hour alignment with Stage 4 baseline (00:00 UTC match)
Duration: Exactly 24 hours (00:00-00:00 UTC)
Comparison: Controlled time-of-day (both runs same UTC hour band)
Gate criteria: Pre-committed, no post-hoc invention


================================================================================
STAGE 4.5 - DETECTION BUG AUDIT AND CORRECTED BASELINE
2026-09-21 06:47:56 UTC
================================================================================

CRITICAL FINDING: Rate-Limit Detection Bug
  Pattern: '429' in line
  False positives: 2,373 matches from '.429xxx' timestamp fractions
  Reality: 0 actual HTTP 429 responses in entire Stage 3/4 history
  Impact: "2.17/hour baseline" was entirely false

SECONDARY FINDING: Timeout Detection Bug
  Pattern: 'Timeout' in line
  Issue: Caught debug traces, connection pool logs, not errors
  Reality: ~0.02/hour real timeout errors

VERIFIED DETECTION: DNS Failures and Drops
  DNS: 'getaddrinfo failed' - specific, no false positives
  Drops: 'Resetting dropped connection' - specific, no false positives

CORRECTED STAGE 4 BASELINE (100 companies, 41.8 hours active)
  Period: 2026-09-19 18:27:01 to 2026-09-21 12:17:34 UTC
  Drop rate: 0.74/hour (verified, fresh computation)
  DNS failures: 3.35/hour (verified)
  Connection drops: 0.74/hour (verified)
  Real rate limits: 0.00/hour (API NOT rate-limiting)
  Timeouts: 0.02/hour (negligible)

STAGE 4.5 EXPECTATIONS (250 companies, if linear scaling 100→250)
  Drop rate: ~0.93/hour (0.74 * 1.25)
  DNS failures: ~4.19/hour (3.35 * 1.25)
  Connection drops: ~0.93/hour (0.74 * 1.25)
  Rate limits: 0.00/hour (no change, API not rate-limiting)

CORRECTED PRE-COMMITTED GATE CRITERIA FOR STAGE 4.5
Written 2026-09-21 06:47 UTC, BEFORE Stage 4.5 launch (2026-09-22 00:00 UTC)
Threshold logic: 1.5x linear maximum for any metric

PASS (proceed to next stage):
  ✓ Drop rate ≤ 1.2/hour (1.5x linear expectation)
  ✓ Connection drops ≤ 1.2/hour
  ✓ DNS failures ≤ 6.0/hour (1.5x linear expectation)
  ✓ No database errors
  ✓ No unexpected rate-limiting (0/hour expected and observed)

YELLOW (continue with caution, flag for review):
  - (Drop 1.2-1.5/h OR Drops 1.2-1.5/h OR DNS 6.0-7.5/h)
  - AND no other critical failures

PAUSE (investigate before proceeding):
  - Drop rate > 1.5/hour (super-linear degradation)
  - OR Connection drops > 1.5/hour
  - OR DNS failures > 7.5/hour
  - OR Database errors present
  - OR Unexpected rate-limiting appears (>0.5/hour would signal new constraint)

KEY CHANGES FROM ORIGINAL CRITERIA:
  - Removed rate-limit gate (was 3.5/h, now 0/h verified baseline)
  - Added explicit DNS gate (4.19/h expected, 6.0/h max)
  - Clarified connection-drop gate (0.74/h expected, 1.2/h max)
  - Drop rate gate unchanged (0.93/h expected, 1.2/h max)

STAGE 4.5 READY FOR LAUNCH
================================================================================


================================================================================
STAGE 4.5 LAUNCH DELAY - DISCIPLINED REALIGNMENT
2026-09-23 07:06:48 UTC
================================================================================

SITUATION:
  Stage 4.5 scheduled launch: 2026-09-22 00:00:00 UTC
  Actual current time: 2026-09-23 07:06:48 UTC
  Status: Launch window MISSED (31+ hours past deadline)
  Stage 4 status: Still running (100 companies, 67+ hours continuous)

DECISION: WAIT FOR NEXT ALIGNED WINDOW (Option B)
  NOT launching misaligned at current time
  REASON: The entire preceding investigation was about fixing measurement
  and timing discipline. Launching 31 hours late would defeat that discipline
  for an 11-hour time savings.

CORRECTED TIMELINE:
  ✓ Stage 4 continues: 2026-09-23 07:06 UTC to 2026-09-24 00:00 UTC (17 hours)
  → Stage 4.5 launch: 2026-09-24 00:00:00 UTC (00:00 UTC aligned)
  → Stage 4.5 window: 2026-09-24 00:00 to 2026-09-25 00:00 UTC (24 hours)
  → Gate decision: 2026-09-25 00:00:00 UTC

LAUNCH SEQUENCE (2026-09-24 00:00:00 UTC):
  1. Confirm Stage 4 process running
  2. Stop run_system.py gracefully
  3. Backup: cp config/watchlist.py config/watchlist_100_stage4_final.py
  4. Swap: cp config/watchlist_250.py config/watchlist.py
  5. Clear: rm state/process_started.txt state/last_processed.txt
  6. Start: python run_system.py
  7. VERIFY: Confirm startup at 00:00:00 UTC exactly
  8. Check: python status.py (confirm 250 companies loaded)

RATIONALE FOR WAITING:
  - Stage 4 has already collected 67+ hours of data (well beyond minimum)
  - The design discipline was UTC hour alignment (00:00-00:00) to control time-of-day
  - Launching misaligned reintroduces the confound we spent effort ruling out
  - Trustworthy comparison requires matching baseline and test windows
  - 11-hour delay is acceptable cost for measurement integrity
  - This is exactly the kind of discipline that prevents false findings

PRE-COMMITTED GATE CRITERIA (unchanged):
  PASS:   Drop ≤1.2/h AND Drops ≤1.2/h AND DNS ≤6.0/h AND no DB errors
  YELLOW: Moderate escalation in any metric
  PAUSE:  Drop >1.5/h OR Drops >1.5/h OR DNS >7.5/h OR DB errors

Stage 4.5 READY FOR ALIGNED LAUNCH
================================================================================


================================================================================
STAGE 4.5 - CORRECTED BASELINE FROM 284-HOUR EXTENDED RUN
2026-10-02 08:13:17 UTC
================================================================================

BASELINE RECOMPUTATION: Full 284-hour run (2026-09-20 17:37 to 2026-10-02 13:42)

KEY FINDING: System stabilized dramatically over time
  Period 1 (first 42 hours):   DNS 1.51/h, Drops 0.26/h
  Period 2 (remaining 242h):   DNS 0.33/h, Drops 0.09/h
  
  Explanation: Startup transients cleared, DNS caching activated, connection pool warmed
  Implication: Later period shows true steady-state behavior at 100 companies

CORRECTED STAGE 4 BASELINE (284 hours):
  Drop rate: 0.116/hour (not 0.740)
  DNS failures: 0.510/hour (not 3.350)
  Connection drops: 0.116/hour
  Real rate limits: 0.000/hour (CONFIRMED)
  Rate limiting detected: ZERO real 429s in entire log
  
  Reliability: 6x longer measurement, captures equilibrium behavior
  Confidence: Very high - 12 days of continuous validation

STAGE 4.5 CORRECTED EXPECTATIONS (linear 100→250, multiply by 1.25):
  Expected drop rate: 0.145/hour (0.116 * 1.25)
  Expected DNS rate: 0.638/hour (0.510 * 1.25)
  Expected connection drops: 0.145/hour
  Expected rate limits: 0.000/hour (still zero)

STAGE 4.5 CORRECTED PRE-COMMITTED GATE CRITERIA
Written 2026-10-02 08:13 UTC, BEFORE Stage 4.5 launch
Threshold logic: 1.5x linear maximum for any metric

PASS (proceed to Stage 5):
  ✓ Drop rate ≤ 0.174/hour (1.5x * 0.116)
  ✓ Connection drops ≤ 0.174/hour
  ✓ DNS failures ≤ 0.766/hour (1.5x * 0.510)
  ✓ No database errors
  ✓ No unexpected rate-limiting (still 0/h)

YELLOW (continue with caution):
  - (Drop 0.174-0.230/h OR Drops 0.174-0.230/h OR DNS 0.766-1.000/h)
  - AND no other critical failures

PAUSE (investigate before proceeding):
  - Drop rate > 0.230/hour (super-linear)
  - OR Connection drops > 0.230/hour
  - OR DNS failures > 1.000/hour
  - OR Database errors
  - OR Unexpected rate-limiting appears (> 0.001/hour would be new)

STAGE 4.5 LAUNCH TIMING:
  Scheduled: 2026-10-03 00:00:00 UTC (next aligned 00:00 UTC window)
  Duration: 24+ hours for measurement
  Gate decision: 2026-10-04 00:00:00 UTC (apply pre-committed criteria)

DISCIPLINE NOTES:
  • Delayed launch again (from 2026-09-22 to 2026-09-24 to 2026-10-03)
  • Maintained UTC hour alignment throughout (00:00 UTC disciplined launches)
  • Recomputed baseline before launch (not inherited from earlier estimate)
  • Found system stabilized 6-7x better than startup transients suggested
  • Gate criteria updated to match actual steady-state behavior
  • All changes locked in BEFORE Stage 4.5 data arrives (no post-hoc adjustment)

STAGE 4.5 READY FOR ALIGNED LAUNCH
================================================================================


================================================================================
STAGE 4.5 - WORKLOAD CONFOUND DETECTED, CRITERIA REVISED
2026-10-02 08:30:00 UTC
================================================================================

CRITICAL FINDING: The 6-7x error improvement was NOT from system stabilization

Workload analysis revealed:
  Period 1 (early, active): 275 API requests/hour
  Period 2 (late, cached): 35 API requests/hour
  Ratio: 7.8x DROP in workload

Error rate changes:
  DNS: 4.5x improvement
  Drops: 2.9x improvement
  
But workload dropped 7.8x, which explains MOST of the improvement.

Normalized analysis (errors per request):
  Period 1: 0.00548 DNS/request, 0.00096 drops/request
  Period 2: 0.00949 DNS/request, 0.00258 drops/request
  
RESULT: Error rate WORSENED per unit of work!
The improvement was cache saturation (fewer new announcements to fetch),
not system reliability improvement. The error rate per request actually got worse.

IMPACT ON STAGE 4.5:
  Stage 4.5 will have 150 NEW companies (fresh announcements, no cache)
  This means Stage 4.5 will do ACTIVE work similar to Period 1, not Period 2
  Using Period 2 baseline would cause false PAUSE on workload increase alone

REVISED STAGE 4 BASELINE (using Period 1 - active workload):
  DNS failures: 1.51/hour (Period 1, not misleading 0.510/h from Period 2)
  Connection drops: 0.26/hour (Period 1, not misleading 0.116/h from Period 2)
  Rate limits: 0.00/hour (confirmed across all periods)

REVISED STAGE 4.5 EXPECTATIONS (250 companies, 1.25x from 100):
  Expected DNS: 1.89/hour (1.51 * 1.25)
  Expected drops: 0.33/hour (0.26 * 1.25)

REVISED PRE-COMMITTED GATE CRITERIA FOR STAGE 4.5
Written 2026-10-02 08:30 UTC, BEFORE Stage 4.5 launch
Threshold logic: 1.5x linear maximum, based on active-workload baseline

PASS (proceed to Stage 5):
  ✓ DNS failures ≤ 2.8/hour (1.51 * 1.5 * 1.25)
  ✓ Connection drops ≤ 0.5/hour (0.26 * 1.5 * 1.25)
  ✓ No database errors
  ✓ No unexpected rate-limiting (still 0/h)

YELLOW (continue with caution):
  - (DNS 2.8-3.5/h OR Drops 0.5-0.65/h)
  - AND no other critical failures

PAUSE (investigate before proceeding):
  - DNS > 3.5/hour
  - OR Connection drops > 0.65/hour
  - OR Database errors
  - OR Unexpected rate-limiting appears

CRITICAL MONITORING REQUIREMENT:
  During Stage 4.5, TRACK THE REQUEST RATE
  If requests drop >5x during the run, errors are expected to drop proportionally
  Example: If requests drop to 50/hour (cache fills), errors expected to drop ~2x
  This is NORMAL and does NOT trigger PAUSE
  
MEASUREMENT DISCIPLINE:
  Extract not just error counts, but also REQUEST counts for Stage 4.5
  Gate decision: Apply error thresholds ONLY if request rate stayed similar to Period 1
  If request rate differs significantly, evaluate on errors-per-request basis instead

STAGE 4.5 READY FOR ALIGNED LAUNCH WITH CORRECTED CRITERIA
================================================================================


================================================================================
STAGE 4.5 - DECISION RULE MECHANIZED (NOT JUDGMENT CALL)
2026-10-02 08:45:00 UTC
================================================================================

GATE DECISION LOGIC - Pre-committed branching rule

At 24-hour mark, extract three numbers:
  1. DNS failure count (total errors in 24h)
  2. Connection drop count (total errors in 24h)
  3. API request count (total GET requests in 24h)

Calculate:
  - errors_per_hour_dns = DNS / 24
  - errors_per_hour_drops = drops / 24
  - errors_per_request_dns = DNS / requests
  - errors_per_request_drops = drops / requests
  - request_rate_per_hour = requests / 24

BRANCHING DECISION RULE (apply ONLY ONE branch):

IF request_rate_per_hour is within 30% of Stage 4 Period 1 baseline (275/h):
  [Request rate is 192-358 requests/hour]
  BRANCH A: Use errors-per-hour thresholds (workload comparable)
  
  PASS if: DNS/h ≤ 2.8 AND Drops/h ≤ 0.5 AND no DB errors AND no rate-limiting
  YELLOW if: (DNS/h 2.8-3.5 OR Drops/h 0.5-0.65) AND no other failures
  PAUSE if: DNS/h > 3.5 OR Drops/h > 0.65 OR DB errors
  
ELSE IF request_rate_per_hour is <192 or >358 requests/hour:
  [Workload significantly different from baseline]
  BRANCH B: Use errors-per-request thresholds (workload-normalized)
  
  Stage 4 Period 1 baseline: 0.00548 DNS/request, 0.00096 drops/request
  Allow 1.5x linear scaling to 250 companies: multiply baselines by 1.5
  Target: 0.00822 DNS/request, 0.00144 drops/request
  
  PASS if: DNS/req ≤ 0.00822 AND Drops/req ≤ 0.00144 AND no DB errors AND no rate-limiting
  YELLOW if: (DNS/req 0.00822-0.01096 OR Drops/req 0.00144-0.00192) AND no other failures
  PAUSE if: DNS/req > 0.01096 OR Drops/req > 0.00192 OR DB errors

DOCUMENT THE DECISION CHAIN:

When reporting Stage 4.5 results, MUST include:
  1. Actual request count and rate (requests/hour)
  2. Which BRANCH was applied (A or B) and why
  3. Metric values for BOTH errors/hour AND errors/request
  4. Applied thresholds (which column was compared)
  5. Gate decision (PASS/YELLOW/PAUSE) with full reasoning
  
This ensures the decision is transparent, reproducible, and defensible.

EXAMPLE OUTCOMES:

Scenario 1: Workload holds steady at ~275 req/h, errors stay low
  Request rate: 268/h [within 30% of 275] -> BRANCH A
  DNS: 2.1/hour, Drops: 0.35/hour [both under thresholds]
  Decision: PASS

Scenario 2: Cache fills, request rate drops to 50/h, errors also drop proportionally
  Request rate: 50/h [outside 30% of 275] -> BRANCH B
  DNS: 275 errors / 120k requests = 0.0023 per request [well under 0.00822]
  Drops: 40 errors / 120k requests = 0.00033 per request [well under 0.00144]
  Decision: PASS (workload normalized, no real degradation)

Scenario 3: Super-linear degradation
  Request rate: 300/h [within 30%] -> BRANCH A
  DNS: 4.2/hour, Drops: 0.8/hour [over 3.5/h and 0.65/h]
  Decision: PAUSE (regardless of request rate, this is super-linear failure)

STAGE 4.5 READY FOR MECHANIZED DECISION PROCESS
================================================================================
