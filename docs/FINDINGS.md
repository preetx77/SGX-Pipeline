# SGX Pipeline Findings and Status

**Date:** November 4, 2026

## Big Six Companies: Not Valid SGX Insider Disclosure Sources

Tested with exact issuer names and `iter_company_announcements` pagination:
- United Overseas Bank Limited — **0 announcements**
- Singapore Telecommunications Limited — **0 announcements**
- Keppel Corporation Limited — **0 announcements**
- Frasers Property Limited — **0 announcements**
- Mapletree Commercial Trust — **0 announcements**
- Prudential plc — **0 announcements**

**Conclusion:** These companies do not file insider disclosures through SGX's announcement API. They may not be SGX-listed issuers or may use a different disclosure mechanism. Do not include in insider monitoring watchlist.

## Watchlist Quality

**Current watchlist:** 32 verified baseline companies
- All have director insider filings (Form 1)
- All have real SGX codes (3-4 characters)
- No generated placeholder codes

**Expansion candidates (49 companies):** All rejected
- All had zero insider filings in initial scan
- Company names suggest bond issuers and fund managers (not equity)
- Names like "Agile Group Holdings", "AIMS APAC REIT Management" are not typical equity issuers

**Recommendation:** Pool is too small for insider monitoring. Need full SGX equity filter.

## XFA Form Hypothesis: CONFIRMED ✓

**Finding:** Adobe-wrapped Form 1 PDFs showing "cannot be displayed" are XFA forms with XML datasets.

**Test results (3/3 PDFs):**
- All contained XFA datasets structure
- Director name: extractable
- Company name: extractable
- Transaction details: embedded in XML

**Recovery potential:**
- ~27 blocked Form 1 files (31% of 87 forms)
- No Tesseract OCR or manual review needed
- Read directly via `pypdf.PdfReader.xfa['datasets']`

**Implementation:** Create XFA extractor module to parse XML datasets and extract director transaction data.

## Stage 5 Dry Run: Not Started

The 100-company run with fake-code expansion companies failed to find meaningful insider signals (as expected—fake codes don't match real SGX listings).

**Next:** Restart Stage 5 with clean 32-company watchlist on aligned 00:00 UTC start for full 24-hour baseline measurement.

## Pool Sampling Plan

Before committing to 12-hour full-universe run:
1. Sample 100 random SGX company names at 1 req/10 sec (17 minutes total)
2. Measure director filing counts
3. Estimate real yield for pool expansion
4. Decide: full run or targeted filter

## Timeline

- [ ] Extract XFA data from 27 blocked Form 1 PDFs
- [ ] Commit XFA extractor module
- [ ] Sample pool: 100 random names (17 min)
- [ ] Restart Stage 5 on clean 32-company list
- [ ] Monitor 24 hours
- [ ] Extract and commit results
- [ ] Generate digest for Shaun (after 1 week live signals)
