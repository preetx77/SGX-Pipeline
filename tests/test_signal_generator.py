import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.announcement_repository import AnnouncementRepository
from database.document_repository import DocumentRepository

from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor
from services.signals.insider_signal_generator import InsiderSignalGenerator


announcement_repo = AnnouncementRepository()
document_repo = DocumentRepository()

extractor = DirectorDealingsExtractor()
generator = InsiderSignalGenerator()

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

    print("=" * 80)
    print("INSIDER SIGNAL")
    print("=" * 80)

    print("Company       :", signal.company_name)
    print("Director      :", signal.director_name)
    print("Transaction   :", signal.transaction_type)
    print("Signal        :", signal.signal)
    print("Signal Type   :", signal.signal_type)
    print("Direction     :", signal.direction)
    print("Importance    :", signal.importance)
    print("Confidence    :", signal.confidence)
    print("Reason        :", signal.reason)

    break