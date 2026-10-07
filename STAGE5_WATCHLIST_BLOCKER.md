# Stage 5 Watchlist: Verification Complete, Code Mapping Pending

## Current Status: 401/401 Companies Verified Real, Codes Not Obtainable via API

### Verification Summary
- ✓ **All 401 new company names** confirmed against SGX /companylist endpoint (4,299 real companies)
- ✓ **Exact match rate**: 100% (all names found in real SGX list)
- ✓ **99 existing companies** have verified ticker codes from database history
- ✗ **401 new company codes** cannot be obtained programmatically from available SGX endpoints

### Technical Blocker
The SGX `/companylist` endpoint returns company **names only**, not ticker codes:
```json
{
  "data": [
    "17LIVE GROUP LIMITED",  // <-- name only, no code
    "1ST SOFTWARE CORPORATION LTD",
    "21VIANET GROUP, INC.",
    ...
  ]
}
```

The announcements API endpoint (`/company`) accepts company names but requires matching them to responses, which times out when queried for 401 companies sequentially due to rate limiting.

### Available Options

#### Option 1: Manual/Bulk Lookup (Medium Effort)
- Use SGX online portal or bulk export to get name→code mapping for all 4,299 companies
- Match the 401 names to codes
- Update watchlist_500_real.py
- **Timeline**: 30-60 minutes
- **Result**: Full Stage 5 with real codes ready to launch

#### Option 2: Launch with Placeholder Codes (Accept Test Limitation)
- Use watchlist_500_real_names.py as-is (401 companies with SGX_REAL_0001..0401 codes)
- Stage 5 will process the 99 real companies successfully
- 401 placeholder codes will error when API is queried (404/Not Found responses)
- **Result**: Stage 5 measures system behavior under 50% failure rate (realistic stress test)
- **Note**: Not a fair scaling measurement, but valid for error handling/stability testing

#### Option 3: Reduce to 99-Company Baseline (No Scaling Test)
- Revert to original 99 validated companies only
- **Result**: No new scaling data beyond Stage 4.5 baseline
- **Impact**: Defeats purpose of Stage 5

### Recommendation
**Option 1**: Invest 30-60 minutes to get a bulk company list with codes from SGX.

This is a one-time infrastructure task that pays off immediately (full Stage 5 launch) and enables any future scaling stages beyond 500.

**Rationale**:
- Option 2 is scientifically invalid (50% fake data, can't isolate real vs. error responses)
- Option 3 is regression (99 < 250 from Stage 4.5 baseline)
- Option 1 is the only path that produces genuine new data

### What Exists Now
- `config/watchlist_500_real_names.py`: 500 real names, 401 placeholder codes
- `match_results_exact.json`: Proof all 401 names are real SGX companies
- `match_company_codes.py`: Script that can incorporate code mapping once available
- `resolve_company_codes.py`: Attempted programmatic resolution (timed out)

### Action Required
1. Obtain SGX company name→code mapping (manually or via bulk export)
2. Run script to merge codes into watchlist_500_real.py
3. Launch Stage 5 with verified 500-company watchlist

**Do not launch Stage 5 with incomplete data.**

---
Status: **BLOCKING** - Code mapping required before Stage 5 launch  
Files ready: config/watchlist_500_real_names.py  
Timeline: 30-60 minutes to complete  
Priority: High - resolves entire scaling validation phase  
