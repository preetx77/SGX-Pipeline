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


