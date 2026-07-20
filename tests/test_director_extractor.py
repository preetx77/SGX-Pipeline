"""
Test the DirectorDealingsExtractor independently.

This avoids going through the EventEngine while developing
the extraction logic.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.announcement_repository import AnnouncementRepository
from database.document_repository import DocumentRepository
from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor


announcement_repo = AnnouncementRepository()
document_repo = DocumentRepository()

extractor = DirectorDealingsExtractor()

announcements = announcement_repo.latest(50)

for announcement in announcements:

    title = announcement.title.lower()

    if (
        "interest" not in title
        and "director" not in title
        and "substantial shareholder" not in title
    ):
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


    print("=" * 80)
    print("Director Dealing Extracted")
    print("=" * 80)

    print("Company   :", dealing.company_name)
    print("Director  :", dealing.director_name)
    print("Date      :", dealing.dealing_date)
    print("Action    :", dealing.action)
    print("Shares    :", dealing.shares)
    print("Price     :", dealing.price)
    print("Value     :", dealing.value)
    print("Currency  :", dealing.currency)
    print("Transaction :", dealing.transaction_type)
    print("Importance  :", dealing.importance)
    print("Before Shares :", dealing.direct_interest_before)
    print("After Shares  :", dealing.direct_interest_after)
