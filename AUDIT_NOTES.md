# Burn-In and Audit Findings

## Burn-In Test Status (as of 2026-08-29)

**CRITICAL: Process crashed on 2026-08-27 at ~22:21 UTC**
- Uptime before crash: ~3 days (not the required 3-7 days clean)
- Root cause: DNS resolution failure for api.sgx.com starting 2026-08-27 19:29
- Error count: 244 (mostly network timeouts, not extraction bugs)
- Status: **INVALID FOR STEP 6 GATE - requires restart and full clean window**

### Action Required
Restart burn-in test and let it run uninterrupted for full 3-7 days before proceeding to Step 6.

---

## Task 1: 7 Blocked Records (No PDF/documents entry)

**Finding: Classifier misclassification bug**

All 6 records with missing PDFs are actually Form 3 filings, not MARKET_PURCHASE:
- `_FORM3_42C_Ong_Kwee_Lin` (42C)
- `_FORM3_5AB_Jun_Oba` (5AB)
- `_FORM3_5AB_Tan_Hun_Tee` (5AB)
- `_FORM3_5AB_Theodore_Goh` (5AB)
- `_FORM3_5TP_Poh_Soon_Keng` (5TP)
- `_FORM3_HQU_Tim_Kusumo` (HQU)

**Root cause**: Classifier incorrectly labeled Form 3 as MARKET_PURCHASE type

**Impact**: 
- No data corruption (just missing PDFs)
- Affects signal classification accuracy once Step 6 expands
- Requires classifier review, not extraction fix

**Action**: Track as known issue, investigate classifier after burn-in completes

---

## Task 2: NULL Director Names

**Finding: No systematic label-wording issue**

Total NULL director names: 2 records
- Both are from corrupted PDFs (Adobe Reader error messages)
- Both are the same records flagged in Phase 4: L208TN0KOAROEIB8

**Cause**:
- L208TN0KOAROEIB8 and EDCOGTI9OD5TYC0D: Corrupted PDF extraction, not label variation

**Eddy Lee status**: Correctly extracted in database (no NULL names for Eddy Lee records)

**Conclusion**: 
- Director name extraction is working correctly
- NULL names only appear on corrupted PDFs (expected)
- No evidence of label-wording variation affecting extraction
- Earlier Form 1 naming gap from earlier investigation was different issue

---

## Summary: What's Ready, What's Blocked

### Ready for Step 6 (when burn-in completes):
- ✓ 20 verified MARKET_PURCHASE records with high-confidence data
- ✓ Extraction code fixes validated
- ✓ Telegram signal format tested

### Blocked Until Burn-In Completes:
- ✗ Step 6 watchlist expansion (needs clean 3-7 day burn-in first)
- ✗ Accuracy reporting to Shaun (need verified uptime numbers)

### Known Issues (non-blocking):
- ⚠️ Classifier misclassification: Form 3 → MARKET_PURCHASE (6 cases)
- ⚠️ DNS resolution to api.sgx.com (intermittent network issue)
- ⚠️ 1 corrupted PDF with false data (L208TN0KOAROEIB8)
- ⚠️ 1 suspiciously small count to manually verify (Kong Wan Sing, 5 shares)

### Next Steps:
1. Restart burn-in test
2. Monitor for full 3-7 day clean window
3. Check periodically: `python status.py` and `tail -50 burn_in_test.log`
4. Once burn-in passes, proceed to Step 6 gradual expansion (12 → 25 → 50 → 100 → full)
5. Before Step 6: Confirm "list all SGX companies" data source exists (or accept manual entry)
