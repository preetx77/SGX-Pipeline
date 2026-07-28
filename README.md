# SGX-Pipeline

A Python system that watches Singapore Exchange (SGX) company announcements in real time. It downloads and reads the attached filings, figures out what type of announcement it is, and turns director share dealings into buy/sell signals. Signals are stored in SQLite and sent to Telegram.

It logs in directly to SGX's internal announcements API instead of scraping the public website.

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

**There are two versions of the insider pipeline right now:**

- `pipeline/sgx_pipeline.py` is the one currently used by `SGXWatcher`. It routes, extracts, classifies, and creates a signal, but does not save anything to the database or guard against duplicates.
- `services/insider_pipeline.py` is a more solid version. It wraps every step in error handling, logs properly instead of using print statements, checks the database first to avoid duplicate signals, and only sends a notification if the signal is actually worth acting on. It is not wired into the watcher yet, but looks like it is meant to replace the current one.

**The watchlist is now a proper data structure**, not just a plain list. `config/watchlist.py` defines a `Company` type with a name, stock code, whether it is enabled, a priority level, and a sector. Right now it covers 12 SGX-listed companies across industries like healthcare, biotech, mining, and real estate.

**The database has grown to 5 tables**: announcements, attachments, documents (which stores the full extracted text, not just metadata), financial metrics, and insider signals (which has a rule built in so the same announcement can never create two signals).

---

## Notable design choices

- **The login method was reverse engineered.** SGX does not give out a public key for this data. `scraper/auth.py` grabs a token from SGX's own QR code system and decodes it to get the real key used for every request.
- **Cheap filtering happens before expensive work.** `AnnouncementRouter` checks a few keywords first, before any PDF is opened or parsed. This means announcements that are not insider dealings never trigger the slower extraction step.
- **Priority is separate from announcement type.** `core/priority.py` keeps this mapping in one place: trading halts and financial results are CRITICAL, insider dealings and acquisitions are HIGH, dividends and board changes are MEDIUM, and buybacks or general announcements are LOW. Changing what gets notified is a one line change, not a rewrite of the rules.
- **Three separate formatters currently exist** for turning an announcement into a Telegram message (`utils/formatter.py`, `watchers/formatter.py`, and `notifications/announcement_builder.py`). They all do roughly the same job. They were most likely written at different points as the project grew, rather than sharing one shared formatter.
- **Logging goes to both the console and a file.** This is built so the system can run unattended for long periods, not just while someone is watching the terminal.

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
```

---

## Current status

The system is live. Insider dealing signals work end to end for a watchlist of 12 companies, with checkpointed polling, proper logging, and protection against duplicate signals. The newer `InsiderPipeline` looks close to replacing the current one. The general classifier in `core/` can sort every announcement type but is not yet driving notifications outside the insider path. Financial results extraction is regex based and only covers revenue and net profit for now.

This is a research and monitoring tool. It is not financial advice.
