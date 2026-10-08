# Stage 5-Corrected Launch Checklist

## Pre-Launch Status: ✅ READY

### Integrity Verification Complete
- ✅ Baseline equity filter: 35/100 companies verified (Form 1/3 filing history)
- ✅ Non-equity identification: 32 companies confirmed (no insider filings)
- ✅ API errors categorized: 33 systematic failures (non-equity name patterns)
- ✅ Expansion rejection: 297 companies, 0% equities (sample), ~85% non-equity (extrapolated)

### Correction Documentation
- ✅ AUDIT_NOTES.md updated with Stage 3-4.5 infrastructure-only measurement clarification
- ✅ Watchlist corrected: 35 verified equities in config/watchlist.py
- ✅ Signal-coverage claims disregarded (contamination discovery made them invalid)
- ✅ Infrastructure findings preserved (DNS, drops, DB concurrency, throttling all valid)

### Files Committed
- ✅ AUDIT_NOTES.md – Correction note prepended
- ✅ config/watchlist.py – Updated with 35 verified equities (Stage 5-Corrected)
- ✅ config/watchlist_stage5_corrected.py – Backup reference
- ✅ baseline_filing_check.json – Verification results (35 with filings, 32 without, 33 errors)
- ✅ BACKGROUND_TASK_EQUITY_FILTER.md – Future expansion foundation (4,299 companies)
- ✅ Git commits: Main branch clean, 2 commits (equity filter + background task)

## Launch Sequence (2026-10-XX 00:00:00 UTC)

1. **Verify Stage 4 completion**
   ```bash
   tail -100 logs/stage4.log | grep "Stage 4 complete\|Final results\|Process exit"
   ```

2. **Stop run_system.py gracefully** (if still running)
   ```bash
   pkill -f run_system.py  # or manual termination
   # Verify: ps aux | grep run_system
   ```

3. **Confirm watchlist configuration**
   ```bash
   python -c "from config.watchlist import WATCHLIST; print(f'Loaded {len(WATCHLIST)} companies')"
   # Expected output: Loaded 35 companies
   ```

4. **Clear state for fresh Stage 5 start**
   ```bash
   rm -f state/process_started.txt state/last_processed.txt
   # Keep database.db (preserve Stage 4 data for reference)
   ```

5. **Start run_system.py for Stage 5**
   ```bash
   nohup python run_system.py > logs/stage5.log 2>&1 &
   # Verify: ps aux | grep run_system
   ```

6. **Verify startup at 00:00:00 UTC exactly**
   ```bash
   head -5 logs/stage5.log | grep "Starting\|Stage 5\|MarketIngestor initialized"
   ```

7. **Monitor Stage 5 measurement window**
   - Duration: 24 hours (2026-10-XX 00:00 to 2026-10-XX+1 00:00 UTC)
   - Watch: DNS failures, connection drops, request rate
   - Expected: DNS 0.5-1.5/h, drops 0.09-0.26/h (linear 0.35x scaling)
   - Expected: API requests ~96/h (35 companies * ~2.7 req/company/hour from Stage 4)

## Gate Decision Criteria (2026-10-XX+1 00:00:00 UTC)

At 24-hour mark, extract from logs:
- Total DNS failures
- Total connection drops
- Total API requests
- Any database errors?
- Any unexpected rate-limiting?

Apply **Stage 4.5 Mechanized Decision Rule** (see AUDIT_NOTES.md):

**PASS** → Proceed to Stage 6-Corrected (equity-only scaling)
- DNS/h ≤ 1.2 (if request rate similar to Stage 4)
- Drops/h ≤ 0.5 (if request rate similar to Stage 4)
- No database errors
- No rate-limiting above 0/h baseline

**YELLOW** → Continue with caution, flag for review
- Moderate escalation, but manageable
- Document findings, proceed to Stage 6-Corrected

**PAUSE** → Investigate before Stage 6
- DNS/h > 1.5 (super-linear degradation)
- Drops/h > 0.65 (super-linear degradation)
- Database errors present
- Unexpected rate-limiting (>0.001/h new)

## Background Task Status
- ✅ BACKGROUND_TASK_EQUITY_FILTER.md specification complete
- 🔄 Scheduled to start: After Stage 5 measurement confirms (non-blocking)
- 📋 Expected output: Tier A (200-500 equities for Stage 6+), Tier B (secondary pool), Tier C (exclusion list)

## Success Indicators
After Stage 5 completes:
1. ✅ System stability maintained at 0.35x scale (35 companies)
2. ✅ DNS and drop rates scale linearly (expected ~0.5-1.5/h DNS, ~0.09-0.26/h drops)
3. ✅ Request rate holds steady (no anomalous cache/workload effects)
4. ✅ No database errors or unexpected rate-limiting
5. ✅ All 35 equities generate announcements/filings as expected
6. ✅ Recommendation: Proceed to Stage 6-Corrected with confidence

---

**Launch authorized by**: Equity Filter Verification (2026-10-08)
**Stage 5-Corrected window**: 2026-10-XX 00:00 to 2026-10-XX+1 00:00 UTC
**Gate decision**: 2026-10-XX+1 00:00 UTC
