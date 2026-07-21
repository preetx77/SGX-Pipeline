import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import TELEGRAM_TOKEN
from config.settings import CHAT_IDS

print("=" * 60)

print("Token Loaded :", TELEGRAM_TOKEN is not None)

print("Chat IDs     :", CHAT_IDS)

print("=" * 60)

