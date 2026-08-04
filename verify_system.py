#!/usr/bin/env python
"""
Comprehensive System Verification Suite
Run this before deployment to verify everything works correctly
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger
setup_logger()

import logging
logging.info("="*80)
logging.info("SYSTEM VERIFICATION SUITE - Starting comprehensive checks")
logging.info("="*80)

PASSED = 0
FAILED = 0
WARNINGS = 0

def test_pass(message):
    global PASSED
    PASSED += 1
    print(f"[PASS] {message}")
    logging.info(f"PASS: {message}")

def test_fail(message):
    global FAILED
    FAILED += 1
    print(f"[FAIL] {message}")
    logging.error(f"FAIL: {message}")

def test_warn(message):
    global WARNINGS
    WARNINGS += 1
    print(f"[WARN] {message}")
    logging.warning(f"WARN: {message}")

# ============================================================================
# VERIFICATION 1: Database Integrity
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION 1: Database Integrity")
print("="*80 + "\n")

try:
    from database.announcement_repository import AnnouncementRepository
    from database.attachment_repository import AttachmentRepository
    from database.insider_signal_repository import InsiderSignalRepository
    
    ann_repo = AnnouncementRepository()
    att_repo = AttachmentRepository()
    sig_repo = InsiderSignalRepository()
    
    # Check announcements
    total_ann = ann_repo.count()
    test_pass(f"Database connected: {total_ann} announcements stored")
    
    if total_ann == 0:
        test_warn("No announcements in database - fresh install")
    else:
        test_pass(f"Database has {total_ann} announcements")
    
    # Check for duplicates
    from database.database import DatabaseManager
    db = DatabaseManager()
    dups = db.fetchone("""
        SELECT COUNT(*) FROM announcements 
        GROUP BY announcement_id 
        HAVING COUNT(*) > 1
    """)
    if dups:
        test_fail(f"DUPLICATE announcements found: {dups[0]}")
    else:
        test_pass("No duplicate announcements")
    
    # Check foreign keys
    orphaned = db.fetchone("""
        SELECT COUNT(*) FROM attachments 
        WHERE announcement_id NOT IN (
            SELECT announcement_id FROM announcements
        )
    """)
    if orphaned and orphaned[0] > 0:
        test_fail(f"ORPHANED attachments: {orphaned[0]}")
    else:
        test_pass("All attachment foreign keys valid")
    
    ann_repo.close()
    att_repo.close()
    sig_repo.close()
    db.close()
    
except Exception as e:
    test_fail(f"Database integrity check failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# VERIFICATION 2: Extraction Quality
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION 2: Extraction Quality")
print("="*80 + "\n")

try:
    from database.document_repository import DocumentRepository
    from models.document import DocumentType
    
    doc_repo = DocumentRepository()
    
    # Get director dealing documents
    docs = doc_repo.get_documents_by_type(DocumentType.DIRECTOR_DEALINGS)
    test_pass(f"Found {len(docs)} director dealing documents")
    
    if len(docs) > 0:
        # Check extraction quality
        extracted_count = sum(1 for d in docs if d.extracted)
        test_pass(f"{extracted_count}/{len(docs)} documents extracted successfully")
        
        # Check text length
        avg_text_length = sum(len(d.text) for d in docs) / len(docs) if docs else 0
        if avg_text_length > 100:
            test_pass(f"Average extracted text: {avg_text_length:.0f} characters")
        else:
            test_warn(f"Low average text length: {avg_text_length:.0f} chars (might be extraction issue)")
        
        # Check for empty documents
        empty_count = sum(1 for d in docs if not d.text or len(d.text) < 50)
        if empty_count > 0:
            test_warn(f"{empty_count} documents with empty/minimal text")
        else:
            test_pass("All documents have substantial extracted text")
            
        # Sample extraction
        sample_doc = [d for d in docs if d.extracted and len(d.text) > 100]
        if sample_doc:
            doc = sample_doc[0]
            print(f"\nSample extraction from {doc.filename}:")
            print(f"  Pages: {doc.page_count}")
            print(f"  Words: {doc.word_count}")
            print(f"  Text preview: {doc.text[:100]}...")
    else:
        test_warn("No director dealing documents to verify")
    
    doc_repo.close()
    
except Exception as e:
    test_fail(f"Extraction quality check failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# VERIFICATION 3: Notification System
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION 3: Notification System")
print("="*80 + "\n")

try:
    from notifications.telegram_notifier import TelegramNotifier
    from config.settings import TELEGRAM_TOKEN, CHAT_IDS
    
    if not TELEGRAM_TOKEN:
        test_fail("Telegram token not configured in .env")
    else:
        test_pass(f"Telegram token configured: {TELEGRAM_TOKEN[:10]}...")
    
    if not CHAT_IDS:
        test_fail("Chat IDs not configured in .env")
    else:
        test_pass(f"Chat IDs configured: {CHAT_IDS}")
    
    try:
        notifier = TelegramNotifier()
        test_pass("Telegram notifier instantiated successfully")
        notifier.close()
    except Exception as e:
        test_fail(f"Failed to instantiate notifier: {e}")
    
except Exception as e:
    test_fail(f"Notification system check failed: {e}")

# ============================================================================
# VERIFICATION 4: API Client
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION 4: API Client")
print("="*80 + "\n")

try:
    from scraper.client import SGXClient
    from config.watchlist import WATCHLIST
    
    client = SGXClient()
    test_pass("SGX API client instantiated")
    
    if len(WATCHLIST) > 0:
        test_pass(f"Watchlist loaded with {len(WATCHLIST)} companies")
        
        # Test API connection with first company
        test_company = WATCHLIST[0]
        try:
            from datetime import datetime, timedelta
            end = datetime.now()
            start = end - timedelta(days=7)
            
            period_start = start.strftime("%Y%m%d_%H%M%S")
            period_end = end.strftime("%Y%m%d_%H%M%S")
            
            logging.info(f"Testing API with {test_company.name}...")
            announcements = client.get_company_announcement(
                test_company.name,
                period_start=period_start,
                period_end=period_end
            )
            test_pass(f"API responsive: {len(announcements)} announcements for {test_company.code}")
        except Exception as e:
            test_fail(f"API call failed: {e}")
    else:
        test_fail("No companies in watchlist")
    
except Exception as e:
    test_fail(f"API client check failed: {e}")

# ============================================================================
# VERIFICATION 5: Services
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION 5: Services")
print("="*80 + "\n")

try:
    from services.announcement_service import AnnouncementService
    from services.attachment_service import AttachmentService
    from services.document_pipeline import DocumentService
    from services.insider_pipeline import InsiderPipeline
    
    test_pass("AnnouncementService imports")
    test_pass("AttachmentService imports")
    test_pass("DocumentService imports")
    test_pass("InsiderPipeline imports")
    
    ann_service = AnnouncementService()
    att_service = AttachmentService()
    doc_service = DocumentService()
    pipeline = InsiderPipeline()
    
    test_pass("All services instantiate successfully")
    
    ann_service.close()
    att_service.close()
    
except Exception as e:
    test_fail(f"Services check failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# VERIFICATION 6: Logging
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION 6: Logging")
print("="*80 + "\n")

try:
    log_path = Path("logs/sgx_pipeline.log")
    if log_path.exists():
        size = log_path.stat().st_size
        test_pass(f"Log file exists: {size:,} bytes")
        
        with open(log_path, 'r') as f:
            lines = f.readlines()
            test_pass(f"Log file has {len(lines):,} entries")
    else:
        test_warn("Log file not yet created")
    
    logging.info("Test logging message")
    test_pass("Logging system working")
    
except Exception as e:
    test_fail(f"Logging check failed: {e}")

# ============================================================================
# VERIFICATION 7: Configuration
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION 7: Configuration")
print("="*80 + "\n")

try:
    from config.settings import ANNOUNCEMENT_API, USER_AGENT
    
    if ANNOUNCEMENT_API:
        test_pass(f"Announcement API configured: {ANNOUNCEMENT_API}")
    else:
        test_fail("Announcement API not configured")
    
    if USER_AGENT:
        test_pass(f"User-Agent configured")
    else:
        test_fail("User-Agent not configured")
    
except Exception as e:
    test_fail(f"Configuration check failed: {e}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION SUMMARY")
print("="*80 + "\n")

print(f"PASSED: {PASSED}")
print(f"FAILED: {FAILED}")
print(f"WARNINGS: {WARNINGS}")
print(f"TOTAL: {PASSED + FAILED + WARNINGS}")

if FAILED == 0:
    print("\n✅ SYSTEM VERIFICATION PASSED - Ready for deployment!")
    sys.exit(0)
else:
    print(f"\n❌ SYSTEM VERIFICATION FAILED - Fix {FAILED} issue(s) before deployment")
    sys.exit(1)
