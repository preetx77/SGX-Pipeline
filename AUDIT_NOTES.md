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
