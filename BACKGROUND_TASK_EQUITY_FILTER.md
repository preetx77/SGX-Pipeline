# Background Task: Full SGX Equity Filter (4,299 Companies)

## Objective
Build a reusable equity-only filter across all 4,299 SGX listed companies to create a foundation for scalable Stage 6+ expansion. Target: identify 200-500 additional genuine equities from beyond the 35 Stage 5 baseline.

## Scope
- Input: SGX Master Company List (4,299 companies)
- Method: Form 1/3 insider-filing history check (same as Stage 5 baseline filter)
- Output: Equity pool (size ~200-500, depends on prevalence of insider disclosure programs)
- Non-blocking: Runs in parallel with Stage 5 measurement; does not delay Stage 5 launch

## Expected Outcome
Partition 4,299 companies into:
- **Tier A (Equities with insider disclosures)**: ~200-500 companies 
  - Use: Future expansion (Stage 6+, controlled scaling)
  - Confidence: Very high (verified by Form 1/3 filing history)
  
- **Tier B (Equities, no insider program)**: ~400-800 companies
  - Use: Secondary pool if Tier A exhausted
  - Confidence: Medium (listed as equity but may lack disclosure mandates)
  
- **Tier C (Non-equity securities)**: ~2,900-3,300 companies
  - Bonds, REITs, bonds-backed securities, foreign listings, etc.
  - Use: Exclusion list (prevent future contamination)
  - Confidence: High (systematic exclusion pattern from API)

## Implementation

### Phase 1: Data Collection (Expected: 4-8 hours wall-clock)
```
for company in sgx.companies:
    try:
        filings = sgx_api.get_form1_form3_history(company.code)
        if len(filings) > 0:
            tier = "A_with_insider_program"
        else:
            tier = "B_no_insider_program"
    except (NoneType, ParsingError):
        # Systematic API failure indicates non-equity security
        tier = "C_non_equity_security"
    
    equity_filter[company.code] = {
        'name': company.name,
        'code': company.code,
        'tier': tier,
        'filing_count': len(filings) if tier != 'C_non_equity_security' else None,
        'timestamp': now(),
    }
```

### Phase 2: Analysis & Categorization (Expected: 1-2 hours)
- Count distribution: A, B, C
- Compare contamination patterns with Stage 5 baseline findings
- Verify systematic exclusion logic (e.g., do all BOND/PERP/etc. names stay in C?)
- Document any anomalies (e.g., high-filing equity in baseline but marked C)

### Phase 3: Output & Integration (Expected: 1-2 hours)
- Generate CSV: `equity_filter_results.csv` (4,299 rows, columns: code, name, tier, filing_count, error_type)
- Generate summary: `equity_filter_summary.md` (tiers counts, distributions, recommendations)
- Generate watchlist Python: `watchlist_4299_tier_a.py` (for future Stage 6+ import)
- Archive baseline_filing_check.json logic for reference

## Scheduling
- **Start**: After Stage 5 launch confirmation (2026-10-XX 00:00 UTC +24 hours)
- **Expected completion**: 2026-10-XX (same day or next day, depending on API rate limits)
- **Cost**: Overhead only (no disruption to Stage 5 measurement)

## Success Criteria
1. ✓ All 4,299 companies categorized into A/B/C tiers
2. ✓ Tier A ≥ 200 companies (sufficient for Stage 6 expansion)
3. ✓ Tier C > 90% of non-equities observed in Stage 4.5 expansion (pattern holds)
4. ✓ CSV and watchlist files generated and committed
5. ✓ Summary doc explains tier distribution and Stage 6 recommendations

## Files Generated
- `equity_filter_results.csv` – Full categorization
- `equity_filter_summary.md` – Analysis and recommendations
- `config/watchlist_4299_tier_a.py` – Ready-to-import for Stage 6+

## Notes
- This task is **not blocking** Stage 5 launch; it runs in parallel
- Results will inform Stage 6+ planning and reduce expansion contamination risk
- Tier A watchlist can be sampled (e.g., first 250) for Stage 6 if full 4,299 too large
