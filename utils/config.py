# config for sgx pipeline : 

BASE_URL = "https://api.sgx.com/announcements/v1.1/company"

DEFAULT_PERIOD_START = "20060707_160000"
DEFAULT_PERIOD_END = "20260708_155959"

DEFAULT_PAGE_SIZE = 100

HEADERS = {
    "Accept ": "*/",
    "Origin ": "https://www.sgx.com",
    "Referer": "https://www.sgx.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}