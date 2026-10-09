# SGX Company Universe Audit Report
Date: 2026-10-08 09:15 UTC
Status: INVESTIGATION COMPLETE

## 1. ORIGINAL 12-COMPANY WATCHLIST PROVENANCE

**Source:** Git history commit 2bf8f43 (2026-07-25 15:09:41)
**Author:** preetx77 (preetsonar77@gmail.com)
**Method:** MANUAL ENTRY (no API or script source documented)

### Original 12 Companies (Verified in Git):
```
1. OILTEK INTERNATIONAL LIMITED           (HQU) - Industrial
2. HYPHENS PHARMA INTERNATIONAL LIMITED    (1J5) - Healthcare
3. LUM CHANG HOLDINGS LIMITED              (L19) - Construction
4. CREATIONS FOOD COMPANY LIMITED          (5FO) - Consumer
5. CNMC GOLDMINE HOLDINGS LIMITED          (5TP) - Mining
6. GRAND BANKS YACHTS LIMITED              (G50) - Marine
7. IX BIOPHARMA LTD                        (42C) - Biotechnology
8. MOOREAST HOLDINGS LTD                   (1V3) - Marine
9. AEDGE GROUP LIMITED                     (1LO) - Technology
10. OLAM GROUP LIMITED                     (VC2) - Agribusiness
11. TREK 2000 INTERNATIONAL LTD            (5AB) - Technology
12. JUSTCO HOLDINGS LIMITED                (41A) - Real Estate
```

**Evidence of Manual Entry:**
- Commit message: "Add 11 new companies to monitoring" (no API mention)
- No code changes in scraper/ or data fetching logic
- Codes hardcoded directly into watchlist.py
- Comment: "Verify later if needed" on AEDGE code (BVT vs 1LO discrepancy)

---

## 2. CURRENT 500-COMPANY WATCHLIST ASSESSMENT

### File: `config/watchlist_500.py`
- **Total entries:** 500
- **Unique codes:** 500 (no duplicate codes found)
- **Unique names:** 500 (no duplicate names found)
- **Placeholder entries:** 401 (82%)
  - Pattern: "SGX LISTED COMPANY 101" through "SGX LISTED COMPANY 500"
  - Codes: AA0, BA1, CA2, ... (synthetic, incremental pattern)
  - **Status: INVALID, NOT REAL SGX COMPANIES**

### Composition:
```
- Stage 1 Baseline:       12 original companies (HQU, 1J5, L19, etc.)
- Stage 1 Expansion:      ~88 verified companies
- Stage 2-3 Expansion:    ~9 more verified companies
- Placeholders:          401 fake "SGX LISTED COMPANY" entries
```

### Validation Status:
✓ Real companies: ~99 entries (verified to have actual SGX codes)
✗ Placeholder companies: 401 entries (synthetic names, invalid codes)
✗ Duplicate risk: None detected (but fake entries don't matter)
✗ Missing fields: None (all have name + code, though many are fake)

---

## 3. OFFICIAL SGX SOURCES INVESTIGATION

### Source 1: SGX Official API
- **Endpoint tested:** https://api.sgx.com/companies (attempted)
- **Response:** HTTP 403 Forbidden
- **Status:** Requires authentication or not public
- **Conclusion:** Not directly accessible without authorization

### Source 2: StocksSG Developer API
- **Documented at:** https://stocks.com.sg/developers
- **Endpoint tested:** https://stocks.com.sg/api/companies
- **Response:** HTTP 404 Not Found
- **Status:** Endpoint does not exist or requires different path
- **Conclusion:** Not available via public API endpoint

### Source 3: SGX Public Company List (Web)
- **Available:** https://www.sgx.com/securities/companies
- **Access:** HTML page, requires scraping
- **Status:** Browser-based, not API
- **Data structure:** Unknown (would require browser testing)
- **Conclusion:** Possible but requires web scraping

### Source 4: Client.py `get_company_list()` Method
- **Location:** scraper/client.py line 114
- **Method:** `self._get("companylist")`
- **Endpoint:** {ANNOUNCEMENT_API}/companylist
- **Status:** Exists in codebase, not yet tested
- **Expected returns:** Likely company names/codes from SGX announcements API
- **Conclusion:** Real source, needs testing

---

## 4. TEST RESULTS

### Test 1: Client.py get_company_list()
- **Status:** NOT YET TESTED
- **Reason:** No production monitoring running, audit-only mode
- **Recommendation:** Test in isolation with timeout protection

### Test 2: Official SGX API
- **Status:** BLOCKED (403 Forbidden)
- **Reason:** Requires authentication or not publicly accessible
- **Alternative:** May be accessible via SGXClient with auth token

### Test 3: StocksSG API
- **Status:** FAILED (404 Not Found)
- **Conclusion:** Developer endpoint documented but non-functional or moved

---

## 5. VALIDATION AGAINST INDEPENDENT SOURCE

### Cross-check: Announcement API vs Watchlist
- **Known equities:** OILTEK (HQU), HYPHENS PHARMA (1J5), etc.
- **Verification method:** Can call announcements API for these codes
- **Result:** These are definitely real (in Stage 4 data collection)
- **Fake entries:** Can call announcements API for "SGX LISTED COMPANY 101" (AA0)
- **Expected result:** Will fail (API returns no announcements for fake codes)

### Classification: Equities vs Other Instruments
- **Equities:** 99 (approximately, based on form presence)
- **Other instruments:** Unknown (REITs, ETFs, warrants, bonds not yet classified)
- **Missing classification:** watchlist_500.py has no instrument_type field
- **Conclusion:** Type information not available in current watchlist

---

## 6. REFERENCE CANDIDATE FILE NOT YET CREATED

**Proposed location:** `data/reference/sgx_company_universe.csv`
**Status:** Ready to create, awaiting source verification
**Required fields:**
- stock_code
- company_name
- instrument_type (if available)
- source
- verified_at
- validation_status

**Current blockers:**
- Official SGX source (companylist API) not yet tested
- StocksSG API endpoint not working
- No authoritative 4,299-company list confirmed

---

## 7. VALIDATION REPORT SUMMARY

| Metric | Value | Status |
|--------|-------|--------|
| Records retrieved | 500 | ⚠️ Partially valid |
| Unique codes | 500 | ✓ No duplicates |
| Invalid entries (placeholders) | 401 | ❌ 82% fake data |
| Verified equities | ~99 | ✓ Estimated valid |
| Missing names | 0 | ✓ All present |
| Missing codes | 0 | ✓ All present |
| Instrument type classified | 0 | ❌ Unknown for all |
| Independently verified | ~12 | ✓ Original baseline |
| Full market coverage claimed | NO | ✓ Correct (not full) |

---

## 8. ANNOUNCEMENT API CLIENT ASSESSMENT

### Method: `get_company_list()` at line 114
```python
def get_company_list(self):
    return self._get("companylist")
```

**Analysis:**
- ✓ Endpoint exists in SGXClient
- ✓ Likely returns company metadata
- ✗ No documented structure or pagination handling
- ✗ No filtering by instrument type
- ✗ Response structure unknown (need to test)

**Capability:** UNKNOWN (needs testing)
**Note:** This is NOT the announcements endpoint; it's a separate company discovery endpoint

---

## 9. UNMODIFIED SYSTEMS (Per Audit Scope)

✓ Polling intervals: NOT CHANGED
✓ Database architecture: NOT CHANGED
✓ Signal extraction: NOT CHANGED
✓ Telegram notifications: NOT CHANGED
✓ No long-running processes launched

---

## SUMMARY & NEXT STEPS

### Findings:
1. **Original 12-company watchlist:** Manually entered, no API source documented
2. **Current 500-company watchlist:** 82% fake entries (placeholders), 18% possibly valid
3. **Official SGX sources:** Blocked (403), not found (404), or untested (API client method)
4. **Best path forward:** Test SGXClient.get_company_list() to validate API capability

### Before Stage 5 Can Safely Use Real 500-Company Subset:

**Required Actions:**
1. Test `SGXClient.get_company_list()` in isolation:
   - Retrieve full response
   - Parse structure
   - Count unique codes
   - Identify instrument types if present
   - Record retrieval date and HTTP status

2. Validate response against known companies:
   - Confirm OILTEK (HQU) in results
   - Confirm HYPHENS PHARMA (1J5) in results
   - Sample 10 random results via announcements API

3. Separate instrument types:
   - Identify which are ordinary equities (not REITs, ETFs, warrants, bonds)
   - Document inclusion rules explicitly
   - Filter to equity-only if applicable

4. Generate reference file:
   - Create `data/reference/sgx_company_universe.csv`
   - Include: code, name, instrument_type, source, verified_at, validation_status
   - Commit with validation report

5. Build new watchlist:
   - Replace 401 placeholders with real verified companies
   - Or reduce to smaller real subset (e.g., 50-100 verified)
   - Document source for each entry

### Exact Next Step:
**Test SGXClient.get_company_list() and report results**
- This is the only actionable path to real data
- All other sources blocked or non-functional
- No long-running system changes required
- Results will determine whether Stage 5 can proceed with real data or must stay with current 35-company equity baseline

---

End of Report
