"""
Test sending a Telegram message with the correct token and chat ID.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.announcement_repository import AnnouncementRepository
from database.document_repository import DocumentRepository
from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor
from services.signals.insider_signal_generator import InsiderSignalGenerator
from notifications.telegram_notifier import TelegramNotifier
from notifications.message_builder import MessageBuilder

CHAT_ID = 1257229548

repo = AnnouncementRepository()
doc_repo = DocumentRepository()
extractor = DirectorDealingsExtractor()
generator = InsiderSignalGenerator()
notifier = TelegramNotifier(chat_id=CHAT_ID)
builder = MessageBuilder()

announcements = repo.latest(50)
count = 0

for announcement in announcements:
    if "interest" not in announcement.title.lower():
        continue
    
    documents = doc_repo.get_documents_by_announcement(announcement.announcement_id)
    if not documents:
        continue
    
    dealing = extractor.extract(announcement, documents[0])
    signal = generator.generate(dealing)
    
    print(f"Generated signal: {signal.company_name}")
    print(f"Message preview:")
    print(builder.build(signal))
    print("\nSending to Telegram...")
    
    try:
        notifier.notify(signal)
        print("✓ Message sent successfully!")
        count += 1
        if count >= 1:
            break
    except Exception as e:
        print(f"✗ Error: {e}")
        break

print(f"\nTotal messages sent: {count}")
