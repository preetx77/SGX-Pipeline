"""
Process a single insider announcement to test the complete flow
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("PROCESSING SINGLE INSIDER ANNOUNCEMENT")
print("=" * 70)

# Find an insider announcement
from database.announcement_repository import AnnouncementRepository
ann_repo = AnnouncementRepository()

all_announcements = ann_repo.latest(200)
insider_announcement = None

for ann in all_announcements:
    if "disclosure of interest" in ann.category.lower():
        insider_announcement = ann
        break

if not insider_announcement:
    print("❌ No insider announcements found")
    sys.exit(1)

print(f"\nProcessing: {insider_announcement.company_name}")
print(f"Title: {insider_announcement.title}")
print(f"ID: {insider_announcement.announcement_id}")

# Process attachments
print("\n[1] Processing attachments...")
from services.attachment_service import AttachmentService
attachment_service = AttachmentService()

try:
    result = attachment_service.process_announcement(insider_announcement)
    print(f"  Attachments found: {len(result['attachments'])}")
    print(f"  Downloaded: {len(result['downloaded'])}")
    print(f"  Failed: {len(result['failed'])}")
    
    if result['failed']:
        for fail in result['failed']:
            print(f"    Failed: {fail['error']}")
    
    attachments = result['downloaded'] + result['existing']
    
    if not attachments:
        print("❌ No attachments available")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Attachment processing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Process documents
print("\n[2] Processing documents...")
from services.document_pipeline import DocumentService
from models.document import DocumentType
document_service = DocumentService()

processed_documents = []

for attachment in attachments:
    try:
        doc_result = document_service.process(insider_announcement, attachment)
        document = doc_result['document']
        print(f"  Document type: {document.document_type}")
        
        if document.document_type == DocumentType.DIRECTOR_DEALINGS:
            processed_documents.append(document)
            print(f"  ✓ Director dealing document")
            
    except Exception as e:
        print(f"  ❌ Document processing failed: {e}")

if not processed_documents:
    print("❌ No director dealing documents found")
    sys.exit(1)

# Process through insider pipeline
print("\n[3] Running insider pipeline...")
from services.insider_pipeline import InsiderPipeline
pipeline = InsiderPipeline()

try:
    pipeline.process(insider_announcement, processed_documents)
    print("✓ Pipeline completed")
    
except Exception as e:
    print(f"❌ Pipeline failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ PROCESSING COMPLETE")
print("=" * 70)
print("\nCheck:")
print("  • Database for saved signal")
print("  • Telegram for notification (if signal was actionable)")
