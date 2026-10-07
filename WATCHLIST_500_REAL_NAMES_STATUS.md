# WATCHLIST INTEGRITY FIX: Stage 5 Blocker

## Problem
Stage 5 was configured to run against `watchlist_500.py`, which contains:
- 99 real companies (verified SGX names and ticker codes)
- 401 fake placeholder entries (named "SGX LISTED COMPANY 101-500")

This makes Stage 5 measurements invalid: ~80% of the watchlist has never been verified to exist.

## Actions Taken
1. ✓ Stopped the running Stage 5 process
2. ✓ Fetched real company list from SGX /companylist endpoint (4,299 total)
3. ✓ Generated `config/watchlist_500_real_names.py` with:
   - 99 existing companies (verified SGX names + real ticker codes)
   - 401 new companies (real names from SGX list + placeholder codes SGX_REAL_0001..0401)

## Current Status: BLOCKED - Placeholder Codes Need Real Ticker Mapping

**To proceed with Stage 5, must choose one:**

### Option A: Accept 99-Company Stage 5 (Minimal Risk)
- Run Stage 5 with only the 99 companies that have verified codes
- Eliminates all placeholder data
- Reduces from planned 500 to 99 (much smaller scale than intended)
- **Recommendation**: Proceed now, then expand later once ticker codes are obtained
- **Impact**: Loses the scaling benefit of 500-company test

### Option B: Map Real Ticker Codes (High Effort, Full Scale)
- Write code to query SGX API for each of 401 company names individually
- Extract the real ticker code for each
- Update watchlist_500_real_names.py with actual codes
- **Effort**: Significant API work, may hit rate limits
- **Timeline**: Unknown (hours to days)
- **Impact**: Full 500-company Stage 5 with all real data

### Option C: Manual Mapping (Medium Effort, Full Scale)
- Look up each of the 401 company names in SGX manual resources
- Build a name→code mapping table
- Apply to watchlist
- **Effort**: Tedious but achievable in ~1-2 hours
- **Impact**: Full 500-company Stage 5 with all real data

## Files Created
- `config/watchlist_500_real_names.py` - 500 companies with real names, placeholder codes for 401
- `create_watchlist_500_real_names.py` - Script that generated the watchlist

## Files NOT Updated
- `run_system.py` - Still imports from `config.watchlist_500` (the fake one)
- Stage 5 process - Stopped and not running

## Recommendation
**Option A: Proceed with 99-company Stage 5 now.** Real 500-company scaling data is better than invalid measurements from 401 fake entries. Once we establish valid 99-company baseline, Option B or C can be tackled separately to expand to 500.

**Updated imports needed for Option A:**
```python
# In run_system.py, change from:
from config.watchlist_500 import WATCHLIST

# To a 99-company set (could be the original watchlist.py or a subset of watchlist_500_real_names.py)
```

---
**Decision**: [ ] Use Option A now, [ ] Complete Option B/C first, [ ] Other

