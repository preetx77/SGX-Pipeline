# SGX Pipeline Findings and Status

**Date:** November 4, 2026 | **Updated:** November 4, 2026 (corrections)

## Big Six Companies: Measurement Failed (Not Confirmed as Null)

Tested with multiple name variations and `iter_company_announcements`:
- United Overseas Bank (UOB) — **0 announcements (measurement failed)**
- Singapore Telecommunications (Singtel) — **0 announcements (measurement failed)**
- Keppel Corporation (Keppel) — **0 announcements (measurement failed)**
- Frasers Property (Frasers) — **0 announcements (measurement failed)**
- Mapletree Commercial Trust — **0 announcements (measurement failed)**
- Prudential plc — **0 announcements (measurement failed)**

**Status:** UNRESOLVED
- Zero results indicate **measurement failure, not absence of filings**
- These are well-known major SGX issuers with documented insider filing activity
- The query is returning no results, suggesting a problem with:
  - Company name format (case, abbreviation)
  - API configuration
  - Time period parameters
  - Or actual API access issue

**Next steps:**
1. Obtain official SGX company list (uppercase names)
2. Re-query with verified names
3. Add assertion to fail on zero results for known major companies

## Watchlist Quality

**Current watchlist:** 32 verified baseline companies
- All have director insider filings (Form 1)
- All have real SGX codes (3-4 characters)
- No generated placeholder codes
- Validator: 100% pass (32/32)

**Expansion candidates (49 companies):** All rejected
- All had zero insider filings in initial scan
- Company names suggest bond issuers and fund managers (not equity)
- Names like "Agile Group Holdings", "AIMS APAC REIT Management" are not typical equity issuers

**Recommendation:** Watchlist is small but verified. Pool needs expansion with proper equity filter.

## XFA Form Hypothesis: Untested (Requires cryptography library)

**Initial test status:** FAILED DUE TO MISSING DEPENDENCY
- XFA_FORM_TEST.json shows all 3 PDFs failed: `cryptography>=3.1 is required for AES algorithm`
- No XFA data was extracted; hypothesis remains untested
- Claims of "74 records recovered" are not backed by committed output files

**Status:** Cannot proceed until cryptography is installed and re-tested
- Re-test on same 3 PDFs
- Compare extracted fields against PDF viewer
- Commit actual extracted data before making claims

**Potential (if hypothesis confirmed):**
- ~27 blocked Form 1 files may be recoverable (31% of 87 forms)
- No Tesseract OCR or admin rights needed
- Read directly via `pypdf.PdfReader.xfa['datasets']`

## Stage 5 Dry Run: Not Started

The previous run with fake-code expansion companies found zero insider signals (expected behavior—fake codes don't match real SGX listings).

**Status:** Ready to restart with clean 32-company watchlist on aligned 00:00 UTC start.

## Timeline

- [ ] **Stage 5 restart:** 32-company watchlist, 00:00 UTC alignment (24 hours, ongoing)
- [ ] Fix big-six query with verified SGX names, re-measure
- [ ] Install cryptography, re-run XFA test, commit actual output
- [ ] Pool sample: 100 random names (17 min, after Stage 5)
- [ ] Integrate XFA ingestion (after Stage 5 baseline)
- [ ] Generate digest for Shaun (after 1 week live signals)

---

**Status:** Watchlist validated and ready for Stage 5. XFA and big-six measurements require corrections before claims can be made.
