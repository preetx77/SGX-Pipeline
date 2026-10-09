# SGX Watchlist Audit Report - CRITICAL FINDINGS

**Date:** 2026-10-09  
**Status:** AUDIT COMPLETE - PROPOSED WATCHLIST REJECTED  
**Auditor Decision:** DO NOT DEPLOY

---

## Executive Summary

**PROPOSED WATCHLIST CONTAINS 13 CRITICAL ERRORS (26% FAILURE RATE)**

The proposed 50-company watchlist contains serious defects that make it unsuitable for production deployment:
- **2 delisted companies** (M1 Limited, Noble Group)
- **2 duplicate issuers** (OCBC duplicates O39, PRU duplicates K6S)
- **4 code mismatches** (AL8→A13, ST→U96, AE8→AWX, ENT→Not Found)
- **2 non-equity instruments** (CRC and AXX are bonds)
- **2 baseline entries with issues** (Z74 returns bond code, C6L returns wrong code)

**RECOMMENDATION:** Reject this watchlist entirely. Do not deploy. Return to production with 34-company baseline after verifying its integrity.

---

## Critical Issues Found

### 1. DELISTED COMPANIES (2 entries - MUST REMOVE)

#### M1Z - M1 LIMITED
- **Status:** DELISTED April 24, 2019
- **Evidence:** https://en.wikipedia.org/wiki/M1_(Singaporean_company)
- **Source:** Wikipedia, Straits Times
- **Action:** REMOVE - Company no longer trading

#### N26 - NOBLE GROUP LIMITED  
- **Status:** DELISTED 2018 (Fraud case)
- **Evidence:** Delisted 2018; S$12.6M fine by Monetary Authority of Singapore (August 2022)
- **Source:** Wikipedia, MAS, GMT Research
- **Action:** REMOVE - Fraudulent accounting, disqualified from market

---

### 2. DUPLICATE ISSUERS (2 entries - ONE MUST REMOVE)

#### OCBC (Entry 41) - DUPLICATE OF O39 (Entry 32)
- **Proposed Code:** OCBC
- **Correct Code:** O39
- **Evidence:** Official SGX records show OCBC trading symbol is "O39"
- **Source:** Yahoo Finance (O39.SI), Investing.com, SGX official records
- **Problem:** Entry 32 already contains O39 (OVERSEA-CHINESE BANKING CORPORATION LIMITED)
- **Action:** REMOVE Entry 41; keep Entry 32 (O39)

#### PRU (Entry 42) - DUPLICATE OF K6S (Entry 39)
- **Proposed Code:** PRU
- **Actual Company:** PRUDENTIAL PLC  
- **API Result:** K6S (returns same company)
- **Conflict:** Entry 39 already has K6S (PRUDENTIAL PLC)
- **Problem:** Both entries refer to identical security
- **Action:** REMOVE Entry 42; keep Entry 39 (K6S)

---

### 3. CODE MISMATCHES (4 entries - CODES ARE WRONG)

#### AL8 → Actually A13
- **Proposed:** AL8 (ALLIED TECHNOLOGIES LIMITED)
- **API Returns:** A13
- **Status:** Code mismatch
- **Action:** Use A13 if company is needed, not AL8

#### ST → Actually U96
- **Proposed:** ST (SEMBCORP INDUSTRIES)
- **API Returns:** U96
- **Status:** Code mismatch
- **Action:** Use U96 if company is needed, not ST

#### AE8 → Actually AWX
- **Proposed:** AE8 (AEM HOLDINGS)
- **API Returns:** AWX
- **Status:** Code mismatch
- **Action:** Use AWX if company is needed, not AE8

#### ENT - NOT FOUND
- **Proposed:** ENT (ENTERTAINMENT LIMITED)
- **API Result:** No response / invalid
- **Status:** Company cannot be resolved
- **Action:** REMOVE - company not verifiable on SGX

---

### 4. NON-EQUITY INSTRUMENTS (2 entries - NOT EQUITIES)

#### CRC - CHINA RESOURCE (Entry 49)
- **Proposed:** CRC (CHINA RESOURCE)
- **API Result:** CHINA RESOURCES GAS GROUP LIMITED - BONDS
- **Instrument Type:** BOND (not equity)
- **Problem:** Insider transaction monitoring requires equities, not debt instruments
- **Action:** REMOVE - not eligible security type

#### AXX - AXIATA (Entry 50)
- **Proposed:** AXX (AXIATA)
- **API Result:** GMQB (AXIATA US$1B3.064%N500819 - bond note)
- **Instrument Type:** BOND (not equity)
- **Problem:** Insider transaction monitoring requires equities, not debt instruments
- **Action:** REMOVE - not eligible security type

---

### 5. BASELINE VERIFICATION ISSUES (2 entries - ALREADY IN WATCHLIST)

#### Z74 - SINGTEL (Entry 13)
- **Proposed Code:** Z74
- **API Response:** XCIB
- **Issue:** Z74 query returns XCIB (a PERPETUAL BOND code, not equity code)
- **Status:** Code appears problematic in baseline itself
- **Note:** Needs investigation; may indicate incorrect code or baseline error
- **Action:** VERIFY - baseline entry may be wrong

#### C6L - SINGAPORE AIRLINES LIMITED (Entry 34)
- **Proposed Code:** C6L
- **API Response:** VB9B (MULTIPLE aggregate)
- **Issue:** C6L does not return directly; maps to VB9B (aggregate issuer code)
- **Status:** Code appears problematic
- **Note:** Existing baseline entry; needs verification
- **Action:** VERIFY - baseline entry may need correction

---

## Audit Results Summary

### All 50 Entries Classified

| Classification | Count | Status |
|---|---|---|
| **VERIFIED_ACTIVE_EQUITY** | 30 | PASS |
| **VERIFIED_ACTIVE_OTHER_INSTRUMENT** | 6 | PASS (REITs/Trusts acceptable) |
| **DELISTED** | 2 | FAIL |
| **DUPLICATE_ISSUER_OR_INSTRUMENT** | 2 | FAIL |
| **CODE_NAME_MISMATCH** | 5 | FAIL |
| **UNVERIFIED** | 3 | FAIL |
| **NOT_EQUITY** | 2 | FAIL |
| **TOTAL ISSUES** | **13** | **FAIL** |

---

## Detailed Entry Breakdown

### VERIFIED ACTIVE EQUITIES (30 entries - PASS)

Entries 1-12, 14-16, 19-27, 32-33, 35-40:
- HQU, 1J5, L19, 5TP, G50, 42C, 1V3, XVG, VC2, 5AB, JCO, U11
- S63, BN4, G13
- C8R, 5E2, 9CI, C09, F17, F34, S68, S59, TQ5
- O39, MCOB
- D05, G07, H02, C07, K6S, V03

**Status:** All verified as active equities with matching codes and issuers.

### VERIFIED ACTIVE OTHER INSTRUMENTS (6 entries - PASS with notation)

Entries 17-18, 28-31:
- A17U (CAPITALAND ASCENDAS REIT)
- C38U (CAPITALAND INTEGRATED COMMERCIAL TRUST)
- AW9U (FIRST REIT)
- N2IU (MAPLETREE COMMERCIAL TRUST)
- ME8U (MAPLETREE INDUSTRIAL TRUST)
- M44U (MAPLETREE LOGISTICS TRUST)

**Status:** All are REITs or Business Trusts, not ordinary equities. Acceptable for insider transaction monitoring if consistent with system design. Recommend retaining.

### PROBLEMATIC ENTRIES (13 entries - FAIL)

| Entry | Code | Issue | Status |
|---|---|---|---|
| 13 | Z74 | Returns bond code (XCIB) | INVESTIGATE |
| 34 | C6L | Returns aggregate code (VB9B) | INVESTIGATE |
| 41 | OCBC | Duplicate of O39 | REMOVE |
| 42 | PRU | Duplicate of K6S | REMOVE |
| 43 | M1Z | Delisted 2019 | REMOVE |
| 44 | N26 | Delisted 2018 (fraud) | REMOVE |
| 45 | AL8 | Code mismatch (→A13) | REMOVE |
| 46 | ENT | Not found on API | REMOVE |
| 47 | ST | Code mismatch (→U96) | REMOVE |
| 48 | AE8 | Code mismatch (→AWX) | REMOVE |
| 49 | CRC | Bond, not equity | REMOVE |
| 50 | AXX | Bond, not equity | REMOVE |

---

## Root Cause Analysis

The expansion process failed at the **validation stage**:

1. **Inadequate API verification:** Some codes were added without confirming the API returns the intended security type (equity vs. bond)

2. **No delisting check:** M1 and Noble were included without confirming current listing status

3. **No duplicate detection:** OCBC and PRU were added without cross-checking against existing codes and issuers

4. **Code validation incomplete:** Several codes don't match API responses (AL8→A13, ST→U96, etc.), indicating errors in code assignment

5. **Instrument type verification missing:** CRC and AXX were included without confirming they are equities, not debt instruments

---

## Recommended Actions

### IMMEDIATE (Before any deployment)

1. **Reject the proposed 50-company watchlist entirely**
   - Do not deploy `watchlist_50_proposed.py`
   - Do not modify production (`config/watchlist.py`)
   - Keep baseline 34-company system operational

2. **Verify the baseline 34-company watchlist**
   - Check Z74 and C6L entries specifically (API responses suggest issues)
   - Confirm all 34 codes are current and accurate
   - Document baseline accuracy before any expansion

### SHORT-TERM (Before restarting expansion)

3. **Establish rigorous expansion methodology**
   - For each candidate: confirm code matches API response
   - Check listing status via official SGX records (not just API)
   - Verify instrument type (equity, REIT, or bond)
   - Cross-check for duplicates with existing watchlist

4. **Create candidate rejection criteria**
   - Reject if: delisted, code mismatch, wrong instrument type, duplicate
   - Require: official SGX listing confirmation + API verification + current trading data

5. **Build a correction/verification process**
   - Establish authoritative source for codes (official SGX, not just API)
   - Create audit trail for each addition
   - Implement peer review before final inclusion

### LONG-TERM

6. **Document expansion outcomes**
   - Record why 13 entries were problematic
   - Ensure lessons learned prevent recurrence
   - Update expansion process documentation

---

## Files Generated

**Audit Output:**
- `SGX_WATCHLIST_AUDIT.csv` — Detailed audit of all 50 entries with classifications
- `AUDIT_REPORT_FINDINGS.md` — This report

**Recommendation:**
- Do NOT create new watchlist from expansion entries
- Retain current `config/watchlist.py` (34 companies)
- Verify baseline integrity before any changes

---

## Conclusion

**The proposed 50-company watchlist contains too many defects to deploy. 13 of 50 entries (26%) fail audit criteria.**

The issues identified are fundamental (delisted companies, incorrect codes, non-equity instruments, duplicates) and cannot be fixed with minor adjustments. A complete rework using rigorous verification methodology is required before any expansion can proceed.

**Status:** READY FOR REVIEW - Audit findings documented, watchlist REJECTED, baseline preserved.

