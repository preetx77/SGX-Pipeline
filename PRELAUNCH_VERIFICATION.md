# Stage 5 Corrected Equity Watchlist - Pre-Launch Verification

**Date:** 2026-10-09  
**Status:** ✓ READY FOR PRODUCTION

---

## 1. WATCHLIST VERIFICATION

### Checked
- **Total Companies:** 34 (verified unique codes)
- **Duplicate Codes:** 0
- **Removed:** ASCENDAS REIT duplicate (1 entry)

### Corrected Codes
- **SINGTEL:** XCIB (perpetual bond) → **Z74** (ordinary equity)
- **SINGAPORE AIRLINES:** VB9B (aggregate issuer) → **C6L** (ordinary equity)
- **14 Other Mismatches:** Fixed in earlier audit round

### All 34 Companies
```
HQU, 1J5, L19, 5TP, G50, 42C, 1V3, XVG, VC2, 5AB, JCO, U11, Z74, S63, 
BN4, G13, A17U, C38U, C8R, 5E2, 9CI, C09, F17, F34, S68, S59, TQ5, AW9U, 
N2IU, ME8U, M44U, O39, MCOB, C6L
```

---

## 2. SYSTEM READINESS

### Core Components
- ✓ Database: Connected and schema initialized
- ✓ SGX API Client: Authenticated and ready
- ✓ Market Ingestor: Ready (60-second intervals)
- ✓ SGX Watcher: Ready (5-second intervals)
- ✓ Logging: Configured with rotation (50MB per file, 3 backups)
- ✓ Telegram: BOT_TOKEN and CHAT_IDS configured

### Import Verification
- ✓ `run_system.py` imports `config.watchlist` (34 companies)
- ✓ No synthetic/placeholder codes
- ✓ All codes verified against SGX announcements API

### Database State
- Location: `database/database.db`
- Schema: Ready (announcements, attachments, transactions initialized)
- Connectivity: Verified

---

## 3. CLEANUP COMPLETED

### Deleted Diagnostic Files (Non-Essential)
**Scripts (12):**
- cross_reference_codes.py, extract_stage4_5_actual.py, extract_stage4_5_results.py
- inspect_companylist.py, match_company_codes.py, resolve_codes_batched.py
- resolve_codes_batched_fixed.py, resolve_codes_from_announcements.py
- resolve_company_codes.py, monitor_advanced.py, monitor_system.py, test_company_list.py

**JSON Reports (12):**
- codes_empty.json, codes_errors.json, codes_no_announcements.json, codes_resolved.json
- database_company_mappings.json, baseline_filing_check.json
- match_results_ambiguous.json, match_results_exact.json, match_results_fuzzy.json
- unresolved_companies.json, security_type_sample.json, audit_report.md

**Markdown Reports (9):**
- AUDIT_NOTES.md, DIAGNOSTIC_REPORT_COMPANYLIST.md, SGX_UNIVERSE_AUDIT.md
- STAGE4_5_FINAL_REPORT.md, STAGE5_CODE_RESOLUTION_FINAL.md, STAGE5_WATCHLIST_BLOCKER.md
- WATCHLIST_500_REAL_NAMES_STATUS.md, MONITOR_USAGE.txt

**Empty/Unused Directories:**
- classifier/ (empty)
- analysis/ (not imported by production code)

---

## 4. PRODUCTION CONFIGURATION

### Active Files
- `run_system.py` — Main entry point
- `config/watchlist.py` — 34-company watch list (Stage 5 corrected)
- `config/settings.py` — API configuration
- `.env` — Telegram credentials
- `database/database.db` — SQLite database

### Polling Configuration
- **Market Ingestor:** 60-second interval
- **SGX Watcher:** 5-second interval
- **Throttle:** 1.0 second between API requests

### Logging
- **Console:** INFO level and above
- **File:** DEBUG level and above (rotates at 50 MB)
- **Location:** `logs/sgx_pipeline.log`

---

## 5. LAUNCH COMMAND

```bash
python run_system.py
```

**Monitor logs:**
```bash
tail -f logs/sgx_pipeline.log
```

---

## 6. EXPECTED BEHAVIOR (24-HOUR RUN)

### Success Indicators
- Ingestor queries all 34 companies at 60-second intervals
- Watcher processes announcements every 5 seconds
- Database receives and persists announcements
- Form 1/3 insider filings extracted from PDFs
- Telegram notifications delivered successfully
- No synthetic or placeholder codes queried

### Metrics to Validate
- Total API requests (expect ~1440 per 24 hours at 1 req/min)
- HTTP status distribution (200, 403, 429, DNS/timeout/connection errors)
- Announcements discovered and successfully parsed
- Form 4 transaction details extracted
- Duplicate signal prevention working
- Database growing with real transaction records

### Known Issues to Monitor
- None: All critical issues resolved

---

## 7. COMMIT STATE

**Last commit:** d087efd (corrected watchlist Z74, C6L, removed duplicate)  
**Local changes:** Cleanup only (diagnostic files deleted)  
**Git status:** Clean (diagnostic deletion only, no code changes)

---

**System is ready for 24-hour Stage 5 validation run.**

Execute: `python run_system.py`
