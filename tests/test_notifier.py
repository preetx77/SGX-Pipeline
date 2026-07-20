import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.announcement_repository import AnnouncementRepository
from database.document_repository import DocumentRepository

from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor
from services.signals.insider_signal_generator import InsiderSignalGenerator
from notifications.rich_console_notifier import RichConsoleNotifier


announcement_repo = AnnouncementRepository()
document_repo = DocumentRepository()

extractor = DirectorDealingsExtractor()
generator = InsiderSignalGenerator()
notifier = RichConsoleNotifier()


announcements = announcement_repo.latest(50)

for announcement in announcements:

    if "interest" not in announcement.title.lower():
        continue

    documents = document_repo.get_documents_by_announcement(
        announcement.announcement_id
    )

    if not documents:
        continue

    dealing = extractor.extract(
        announcement,
        documents[0]
    )

    signal = generator.generate(dealing)

    notifier.notify(signal)

    break