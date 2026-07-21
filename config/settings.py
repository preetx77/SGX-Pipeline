# global project config : 

CMS_BASE_URL = "https://api2.sgx.com/content-api/"

ANNOUNCEMENT_API = "https://api.sgx.com/announcements/v1.1"

CMS_VERSION = "70f75ec90c030bab34d750ee55d74b016f70d4b6"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)

# =============================================================================
# Environment Configuration
# =============================================================================

import os
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


CHAT_IDS = [

    int(chat.strip())

    for chat in os.getenv("CHAT_IDS", "").split(",")

    if chat.strip()

]