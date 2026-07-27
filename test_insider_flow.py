"""
End-to-End Test: Insider Announcement Flow
Tests the complete pipeline from announcement detection to Telegram notification
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("INSIDER FLOW END-TO-END TEST")
print("=" * 70)

# Step 1: Find an insider announcement
print("\n[Step 1] Finding insider announcement...")
from database.announcement_repository import AnnouncementRepository
ann_repo = AnnouncementRepository()

all_announcements = ann_repo.latest(200)
insider_announcement = None

for ann in all_announcements:
    if "disclosure of interest" in ann.category.lower():
        insider_announcement = ann
        print(f"✓ Found: {ann.company_name}")
        print(f"  Title: {ann.title}")
        print(f"  ID: {ann.announcement_id}")
        break

if not insider_announcement:
    print("❌ No insider announcements found")
    print("   Run 'python run_system.py' first to fetch announcements")
    sys.exit(1)

# Step 2: Check for documents
print("\n[Step 2] Checking for PDF documents...")
from database.document_repository import DocumentRepository
doc_repo = DocumentRepository()

documents = doc_repo.get_documents_by_announcement(insider_announcement.announcement_id)
print(f"Documents found: {len(documents)}")

if not documents:
    print("❌ No documents found for this announcement")
    print("   Documents may not have been downloaded yet")
    sys.exit(1)

document = documents[0]
print(f"✓ Document type: {document.document_type}")
print(f"  Content length: {len(document.text) if document.text else 0} chars")

# Step 3: Extract dealing from document
print("\n[Step 3] Extracting director dealing...")
from extractors.insider.director_dealings_extractor import DirectorDealingsExtractor
extractor = DirectorDealingsExtractor()

try:
    dealing = extractor.extract(insider_announcement, document)
    print(f"✓ Extracted dealing:")
    print(f"  Director: {dealing.director_name}")
    print(f"  Transaction: {dealing.transaction_type}")
    print(f"  Shares: {dealing.shares}")
    print(f"  Value: ${dealing.value:,.2f}" if dealing.value else "  Value: N/A")
except Exception as e:
    print(f"❌ Extraction failed: {e}")
    sys.exit(1)

# Step 4: Generate signal
print("\n[Step 4] Generating insider signal...")
from services.signals.insider_signal_generator import InsiderSignalGenerator
generator = InsiderSignalGenerator()

try:
    signal = generator.generate(dealing)
    print(f"✓ Signal generated:")
    print(f"  Signal: {'YES' if signal.signal else 'NO'}")
    print(f"  Direction: {signal.direction}")
    print(f"  Signal Type: {signal.signal_type}")
    print(f"  Confidence: {signal.confidence}%")
    print(f"  Reason: {signal.reason}")
except Exception as e:
    print(f"❌ Signal generation failed: {e}")
    sys.exit(1)

# Step 5: Build Telegram message
print("\n[Step 5] Building Telegram message...")
from notifications.message_builder import MessageBuilder
builder = MessageBuilder()

try:
    message = builder.build(signal)
    print("✓ Message built:")
    print("-" * 70)
    print(message)
    print("-" * 70)
except Exception as e:
    print(f"❌ Message building failed: {e}")
    sys.exit(1)

# Step 6: Test notification (dry run)
print("\n[Step 6] Testing Telegram notifier (DRY RUN)...")
print("Would send to Telegram:")
print(f"  Signal active: {signal.signal}")
print(f"  Should notify: {'YES' if signal.signal else 'NO (not actionable)'}")

if signal.signal:
    print("\n⚠️  To actually send, the insider_pipeline would call:")
    print("     self.notifier.notify(signal)")

print("\n" + "=" * 70)
print("✅ END-TO-END TEST COMPLETE")
print("=" * 70)
print("\nConclusion:")
print("  • Announcement detection: ✓")
print("  • Document retrieval: ✓")
print("  • Dealing extraction: ✓")
print("  • Signal generation: ✓")
print("  • Message formatting: ✓")
print("  • Telegram notification: Ready")
