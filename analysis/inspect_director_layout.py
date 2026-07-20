"""
Inspect a Director Dealings document.

Goal: Understand the PDF layout before writing extraction logic.
"""

import sys
from pathlib import Path

# Add parent directory to path so imports work from any location
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.announcement_repository import AnnouncementRepository
from database.document_repository import DocumentRepository


announcement_repo = AnnouncementRepository()
document_repo = DocumentRepository()

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

    document = documents[0]

    print("=" * 100)
    print("TITLE")
    print(announcement.title)
    print()

    print("CATEGORY")
    print(announcement.category)
    print()

    print("FILE")
    print(document.filename)
    print()

    print("=" * 100)
    print(document.text[:8000])
    print("=" * 100)

    break