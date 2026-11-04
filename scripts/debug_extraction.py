"""
Debug: Check what's being extracted from the PDF
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database.document_repository import DocumentRepository
from database.announcement_repository import AnnouncementRepository

# Get an insider announcement
ann_repo = AnnouncementRepository()
anns = ann_repo.latest(50)
insider = [a for a in anns if 'interest' in a.category.lower()][0]

print(f"Announcement: {insider.title}")
print(f"ID: {insider.announcement_id}\n")

# Get its documents
doc_repo = DocumentRepository()
docs = doc_repo.get_documents_by_announcement(insider.announcement_id)

if not docs:
    print("No documents found")
    sys.exit(1)

doc = docs[0]
print(f"Document: {doc.filename}")
print(f"Pages: {doc.page_count}")
print(f"Words: {doc.word_count}")
print(f"Type: {doc.document_type}")
print(f"\nText content (first 1000 chars):")
print("=" * 70)
print(doc.text[:1000] if doc.text else "NO TEXT")
print("=" * 70)

# Try extraction
print("\nAttempting extraction...")
from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor

extractor = DirectorDealingsExtractor()
dealing = extractor.extract(insider, doc)

print(f"\nExtracted:")
print(f"  Director: {dealing.director_name}")
print(f"  Transaction: {dealing.transaction_type}")
print(f"  Shares: {dealing.shares}")
print(f"  Price: {dealing.price}")
print(f"  Value: {dealing.value}")
print(f"  Importance: {dealing.importance}")
