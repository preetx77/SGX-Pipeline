# Stage 4 (100 companies) - Decision Criteria

**Baseline from Stage 3 (50 companies, 31.6 hours):**
- Drop rate: 1.14 drops/hour
- Expected at 100 companies (2x load): ~2.3 drops/hour (linear scaling)
- Correlation: 100% of drops within ±30 seconds of requests

**Stage 4 Thresholds (decided in advance):**

## Drop Rate (Primary Signal)

| Observed Rate | Scaling Factor | Decision |
|---|---|---|
| 1.5 - 2.5 drops/hour | 1.3x - 2.2x | ✓ **PASS** - Linear or sub-linear. Continue. |
| 2.5 - 3.5 drops/hour | 2.2x - 3.1x | ⚠ **YELLOW** - Slightly super-linear. Document but continue to 4,290 observation. |
| 3.5 - 4.5 drops/hour | 3.1x - 4.0x | 🔴 **PAUSE** - Disproportionate scaling. Investigate before full market. |
| >4.5 drops/hour | >4.0x | 🔴 **STOP** - Catastrophic scaling. Do not proceed to Stage 5. |

**Rationale for thresholds:**
- 2.2x-2.5x: Acceptable variance, normal under increased load
- 2.5x-3.1x: Concerning but not disqualifying; suggests load sensitivity starting to show at edges
- 3.1x+: Indicates non-linear problem that will worsen at 4,290; pause to understand

## Correlation Pattern (Secondary Signal)

| Finding | Decision |
|---|---|
| 90-100% correlation (±30s window) | ✓ Continue. Load-related, throttling working as expected. |
| 70-90% correlation | ⚠ Some scatter emerging at higher load, but still manageable. Document. |
| <70% correlation | 🔴 Pattern breaking down. Suggests different failure mode at scale. Investigate. |

## Database Stability (Gating Condition)

| Finding | Decision |
|---|---|
| Zero lifecycle errors (Cannot operate on closed database, recursive cursor) | ✓ Pass. |
| Any lifecycle errors | 🔴 Halt. Database fix didn't hold at 100 companies. Revert or redesign. |

## DNS/Rate-Limit Ratio (Comparative, not gating)

| Finding | Action |
|---|---|
| Rate limits ~2x of Stage 3 (linear) | Expected. Note. |
| Rate limits >2x but <3x | Slightly above linear. May indicate API edge proximity. Note. |
| Rate limits 3x+ or DNS failures spike unexpectedly | Flag as edge case for 4,290 planning. |

---

## Final Stage 4 Gate Decision:

**PASS Stage 4 → Stage 5 if:**
- Drop rate ≤ 3.5 drops/hour (3.1x acceptable threshold)
- AND correlation ≥ 70% (pattern holds or degrades gradually)
- AND zero database lifecycle errors
- AND no unexpected DNS failure spike

**YELLOW (Continue with caution):**
- If 2.5-3.5 drops/hour + correlation still >70% + no DB errors
- Document as "acceptable but monitoring closely for Stage 5"
- Recommend monitoring even more granularly in Stage 5

**PAUSE (Investigate):**
- If drops >3.5 drops/hour OR correlation <70% OR DB errors
- Stop at 100 companies
- Investigate scaling degradation
- Decide on PostgreSQL migration vs. architecture redesign

**STOP (Do not proceed):**
- If drops >4.5 drops/hour (definitively non-linear)
- OR persistent lifecycle errors (DB fix didn't hold)
- Document finding and halt expansion plan

---

## Metrics to Record at 24-hour mark:

1. Exact drop count and time window (calculate drops/hour)
2. Sample of 10 drops with ±30s request windows (paired timestamps)
3. % of drops with requests within ±30s
4. Total API requests logged
5. Error breakdown: DNS, rate limits, timeouts, database
6. Any new error types not seen in Stage 3

This data will be compared against Stage 3 baseline exactly as stated above.
