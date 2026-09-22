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
