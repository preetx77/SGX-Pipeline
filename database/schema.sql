CREATE TABLE IF NOT EXISTS announcements (

    announcement_id TEXT PRIMARY KEY,

    ref_id TEXT,

    company_name TEXT,

    stock_code TEXT,

    isin_code TEXT,

    issuer_name TEXT,

    title TEXT,

    category TEXT,

    category_code TEXT,

    subcategory_code TEXT,

    announcement_url TEXT,

    submission_date TEXT,

    submission_timestamp INTEGER,

    submitted_by TEXT,

    local_path TEXT,

    downloaded INTEGER DEFAULT 0,

    parsed INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

);

-- removed scraped_at : because we should distinguish : submission time -> when sgx publsished it
-- and created time -> when our database inserted it


CREATE TABLE IF NOT EXISTS attachments (

    attachment_id TEXT PRIMARY KEY,

    announcement_id TEXT NOT NULL,

    filename TEXT,

    download_url TEXT,

    file_size TEXT,

    local_path TEXT,

    downloaded INTEGER DEFAULT 0,

    created_at TEXT,

    FOREIGN KEY (announcement_id)
        REFERENCES announcements(announcement_id)
);

-- why second table : 
-- because one announcement can have multiple attachments

CREATE TABLE IF NOT EXISTS documents (

    attachment_id TEXT PRIMARY KEY,

    announcement_id TEXT,

    company_name TEXT,

    stock_code TEXT,

    announcement_title TEXT,

    announcement_category TEXT,

    filename TEXT,

    local_path TEXT,

    page_count INTEGER,

    word_count INTEGER,

    document_type TEXT,

    extracted INTEGER,

    extracted_text TEXT,

    created_at TEXT
);

CREATE TABLE IF NOT EXISTS financial_metrics (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    announcement_id TEXT,

    stock_code TEXT,

    company_name TEXT,

    metric_name TEXT,

    metric_value REAL,

    reporting_period TEXT,

    currency TEXT,

    created_at TEXT

);