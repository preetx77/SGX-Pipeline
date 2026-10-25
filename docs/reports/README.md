# SGX-Pipeline
A Python system that watches Singapore Exchange (SGX) company announcements in real time. It downloads and reads the attached filings, figures out what type of announcement it is, and turns director share dealings into buy/sell signals. Signals are stored in SQLite and sent to Telegram.
It logs in directly to SGX's internal announcements API instead of scraping the public website.

---
## Current Phase: Staged Scaling Investigation (Stage 4.5)

**Goal:** Scale the pipeline from 12→25→50→100→250→500→4,290 companies with stability validation at each gate.

**Methodology:** Controlled, time-windowed stages with pre-committed gate criteria. Each stage validates:
- Drop rate (connection failures per hour)
- DNS failure rate and clustering behavior
- Database lifecycle integrity
- Linear vs super-linear scaling patterns

**Current Status:**
- Stage 1 (12 companies): ✓ PASSED - 839+ hours stable
- Stage 2 (25 companies): ✓ PASSED - Restart-resilient
- Stage 3 (50 companies): ✓ PASSED - 24+ hours, 100% drop correlation, throttling validated
- Stage 4 (100 companies): ✓ PASSED - 41.8+ hours, corrected baseline established
- **Stage 4.5 (250 companies):** IN PROGRESS - 24-hour controlled time-window test

**Latest Findings:**
- Measurement bug discovered: Rate-limit detection was catching `.429` timestamp fractions, not real API 429s
  - Reality: 0 actual 429s across entire Stage 3/4 history
  - API is NOT rate-limiting at current scales
- Corrected Stage 4 baseline (100 companies):
  - Drop rate: 0.74/hour
  - DNS failures: 3.35/hour
  - Connection drops: 0.74/hour
  - Real rate limits: 0.00/hour

**Next Stage:**
- Stage 4.5 gate decision: 2026-09-23 00:00 UTC
- If PASS: Proceed to Stage 5 (500-1000 companies) or Stage 5.5
- No direct jump to 4,290 - violates staged approach

---
## How it works
```
                    run_system.py (main entrypoint)
                    starts two background loops
                              |
              ------------------------------------
              |                                    |
      MarketIngestor (every 60s)          SGXWatcher (every 5s)
      pulls market/company data           checks for new announcements
                                                    |
                                          SGXPipeline.process()
                                                    |
                                    AnnouncementRouter checks if it
                                    is an insider dealing announcement.
                                    If not, it is skipped for now.
                                                    |
                                    DirectorDealingsExtractor
                                    pulls out director name, date,
                                    shares, interest before and after
                                                    |
                                    DirectorDealingsClassifier
                                    figures out the transaction type:
                                    market buy/sell, off-market,
                                    bonus, rights, share award, etc.
                                                    |
                                    InsiderSignalGenerator
                                    creates a signal with direction,
                                    confidence score, and a reason
                                                    |
                    ----------------------------------------
                    |                                        |
        InsiderSignalRepository                    TelegramNotifier
        saves to SQLite, skips duplicates          sends the alert if the
                                                    signal is actionable
```
There is also a separate, more general classifier in `core/`. It looks at every announcement, not just insider dealings, and sorts it into one of eleven types: financial results, trading halt, acquisition, buyback, rights issue, dividend, AGM, board changes, or general. Each type gets a priority level (CRITICAL, HIGH, MEDIUM, or LOW) with a star rating and a flag for whether it should trigger a notification. This is the groundwork for expanding the pipeline to more than just insider signals later.

---
## What is actually running
**`run_system.py`** is the real entrypoint. It starts the market ingestor and the SGX watcher as two background threads in one process, with proper shutdown handling and logging to both the console and a log file. `run_service.py` and `run_ingestor.py` are older, simpler versions kept around for standalone use or debugging.

**Throttling:** 1 second between API requests to respect rate limits and avoid overwhelming SGX's servers.

**There are two versions of the insider pipeline right now:**
- `pipeline/sgx_pipeline.py` is the one currently used by `SGXWatcher`. It routes, extracts, classifies, and creates a signal, but does not save anything to the database or guard against duplicates.
- `services/insider_pipeline.py` is a more solid version. It wraps every step in error handling, logs properly instead of using print statements, checks the database first to avoid duplicate signals, and only sends a notification if the signal is actually worth acting on. It is not wired into the watcher yet, but looks like it is meant to replace the current one.

**The watchlist is now a proper data structure**, not just a plain list. `config/watchlist.py` defines a `Company` type with a name, stock code, whether it is enabled, a priority level, and a sector. Multiple watchlist sizes exist:
- `config/watchlist.py`: Current active watchlist (currently 100 companies)
- `config/watchlist_100.py`: Stage 4 baseline (100 companies, backup)
- `config/watchlist_250.py`: Stage 4.5 test (250 companies)

**The database has grown to 5 tables**: announcements, attachments, documents (which stores the full extracted text, not just metadata), financial metrics, and insider signals (which has a rule built in so the same announcement can never create two signals).

**Database architecture:** Each repository creates its own DatabaseManager (separate SQLite connections per thread). SQLite supports multiple connections with WAL mode and timeout handling for coordination. No shared cursors - each connection manages its own lifecycle.

---
## Notable design choices
- **The login method was reverse engineered.** SGX does not give out a public key for this data. `scraper/auth.py` grabs a token from SGX's own QR code system and decodes it to get the real key used for every request.
- **Cheap filtering happens before expensive work.** `AnnouncementRouter` checks a few keywords first, before any PDF is opened or parsed. This means announcements that are not insider dealings never trigger the slower extraction step.
- **Priority is separate from announcement type.** `core/priority.py` keeps this mapping in one place: trading halts and financial results are CRITICAL, insider dealings and acquisitions are HIGH, dividends and board changes are MEDIUM, and buybacks or general announcements are LOW. Changing what gets notified is a one line change, not a rewrite of the rules.
- **Three separate formatters currently exist** for turning an announcement into a Telegram message (`utils/formatter.py`, `watchers/formatter.py`, and `notifications/announcement_builder.py`). They all do roughly the same job. They were most likely written at different points as the project grew, rather than sharing one shared formatter.
- **Logging goes to both the console and a file.** This is built so the system can run unattended for long periods, not just while someone is watching the terminal.
- **Time-of-day confounds are controlled explicitly.** Staged tests run during matching UTC hours to isolate load effects from network/time-of-day variance. Anomalous periods are identified and excluded from baseline calculations.
- **Measurement logic is audited for false positives.** Detection patterns are kept specific (e.g., `'HTTP/1.1" 429'` for rate-limits, not `'429' in line`) to avoid counting debug logs, timestamps, or announcement titles as errors.

---
## Folder guide
```
core/           Event types, priority rules, the general classifier
pipeline/       AnnouncementRouter and the current SGXPipeline
services/       The newer InsiderPipeline, plus syncing and market data services
scraper/        Login, API client, PDF downloader, HTML parser
extractors/     Turns PDFs into text, then text into structured data
classifiers/    Rule based classification of document and transaction type
parsers/        Reads financial statement sections and rows
events/         Handlers for director dealings, dividends, and financial results
models/         Data classes like Announcement, Document, InsiderSignal, Company
database/       SQLite repositories and schema
notifications/  Telegram and console notifiers, plus the message formatters
utils/          Logging setup and message formatting
state/          Keeps track of the last processed announcement
watchers/       The main polling loop
tests/          Unit tests for each part of the system
analysis/       Small scripts used to inspect extracted data while developing
config/         Watchlist definitions and configuration
logs/           Live process logs (rotated, with historical backups)
```

---
## Running it
Install dependencies:
```bash
pip install -r requirements.txt
```
Add `TELEGRAM_BOT_TOKEN` and `CHAT_IDS` to a `.env` file. Then run one of:
```bash
python run_system.py       # full system: both loops, with logging
python run_service.py      # just the watcher
python run_ingestor.py     # just the market data ingestion
python main.py             # one time historical backfill for a stock
python status.py           # check current process status and metrics
python monitoring.py       # 12-hour window monitoring report
```

---
## Monitoring & Analysis
**Live monitoring:**
```bash
python status.py           # Real-time health check
python monitoring.py       # Last 12 hours of metrics
```

**Key files:**
- `logs/sgx_pipeline.log` - Current session logs (rotated files: .log, .log.2, .log.3)
- `AUDIT_NOTES.md` - Detailed investigation log, baseline corrections, gate decisions
- `STAGE4_DECISION_CRITERIA.md` - Pre-committed gate thresholds and decision logic

---
## Testing & Validation
Each stage validates:
1. **Stability:** Process runs continuously without crashes
2. **Database integrity:** No lifecycle errors, proper connection handling
3. **Scaling linearity:** Does drop rate scale proportionally with company count?
4. **Time-of-day effects:** Does error rate vary by time independent of load?
5. **Correlation patterns:** Are drops correlated with API requests (within ±30s)?

Gate criteria are pre-committed BEFORE each stage runs, not adjusted after data arrives.

---
## Current status
**Stage 4 (100 companies):** Completed with corrected baseline (0.74/h drops, 3.35/h DNS, 0/h real rate limits)

**Stage 4.5 (250 companies):** In progress. 24-hour window runs 2026-09-22 00:00 to 2026-09-23 00:00 UTC. Results will be evaluated against pre-committed PASS/YELLOW/PAUSE gates.

**Next decision:** 2026-09-23 00:00 UTC. If PASS, proceed to Stage 5 (~500 companies or full market expansion).

This is a research and monitoring tool. It is not financial advice.
