#!/usr/bin/env python
"""Test environment and dependencies"""

import sys
from pathlib import Path

# Test 1: Database Connection
print("\n" + "="*60)
print("TEST 1: Database Connection")
print("="*60)
try:
    from database.database import DatabaseManager
    db = DatabaseManager()
    print("✅ Database connection established")
    
    tables = db.fetchall("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [row[0] for row in tables]
    print(f"✅ Tables found: {', '.join(table_names)}")
    
    # Count rows in each table
    for table in table_names:
        count = db.fetchone(f"SELECT COUNT(*) FROM {table}")
        print(f"   - {table}: {count[0]} rows")
    
    db.close()
except Exception as e:
    print(f"❌ Database error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Configuration Loading
print("\n" + "="*60)
print("TEST 2: Configuration Loading")
print("="*60)
try:
    from config.settings import TELEGRAM_TOKEN, CHAT_IDS, ANNOUNCEMENT_API
    
    if TELEGRAM_TOKEN:
        token_preview = TELEGRAM_TOKEN[:10] + "..." + TELEGRAM_TOKEN[-5:]
        print(f"✅ Telegram token configured: {token_preview}")
    else:
        print("❌ Telegram token NOT configured")
    
    if CHAT_IDS:
        print(f"✅ Chat IDs configured: {CHAT_IDS}")
    else:
        print("❌ Chat IDs NOT configured")
    
    print(f"✅ API endpoint: {ANNOUNCEMENT_API}")
except Exception as e:
    print(f"❌ Configuration error: {e}")

# Test 3: Watchlist
print("\n" + "="*60)
print("TEST 3: Watchlist")
print("="*60)
try:
    from config.watchlist import WATCHLIST
    print(f"✅ Watchlist loaded with {len(WATCHLIST)} companies:")
    for company in WATCHLIST[:5]:
        print(f"   - {company.name} ({company.code})")
    if len(WATCHLIST) > 5:
        print(f"   ... and {len(WATCHLIST) - 5} more")
except Exception as e:
    print(f"❌ Watchlist error: {e}")

# Test 4: Repository Classes
print("\n" + "="*60)
print("TEST 4: Repository Classes")
print("="*60)
try:
    from database.announcement_repository import AnnouncementRepository
    repo = AnnouncementRepository()
    count = repo.count()
    print(f"✅ AnnouncementRepository: {count} announcements in database")
    repo.close()
except Exception as e:
    print(f"❌ AnnouncementRepository error: {e}")

try:
    from database.attachment_repository import AttachmentRepository
    repo = AttachmentRepository()
    print(f"✅ AttachmentRepository: accessible")
    repo.close()
except Exception as e:
    print(f"❌ AttachmentRepository error: {e}")

try:
    from database.insider_signal_repository import InsiderSignalRepository
    repo = InsiderSignalRepository()
    print(f"✅ InsiderSignalRepository: accessible")
    repo.close()
except Exception as e:
    print(f"❌ InsiderSignalRepository error: {e}")

# Test 5: Service Classes
print("\n" + "="*60)
print("TEST 5: Service Classes")
print("="*60)
try:
    from scraper.client import SGXClient
    client = SGXClient()
    print(f"✅ SGXClient: instantiated")
except Exception as e:
    print(f"❌ SGXClient error: {e}")

try:
    from services.announcement_service import AnnouncementService
    service = AnnouncementService()
    print(f"✅ AnnouncementService: instantiated")
    service.close()
except Exception as e:
    print(f"❌ AnnouncementService error: {e}")

try:
    from services.attachment_service import AttachmentService
    service = AttachmentService()
    print(f"✅ AttachmentService: instantiated")
    service.close()
except Exception as e:
    print(f"❌ AttachmentService error: {e}")

# Test 6: Notification Service
print("\n" + "="*60)
print("TEST 6: Notification Service")
print("="*60)
try:
    from notifications.telegram_notifier import TelegramNotifier
    notifier = TelegramNotifier()
    print(f"✅ TelegramNotifier: instantiated")
    notifier.close()
except Exception as e:
    print(f"❌ TelegramNotifier error: {e}")

# Test 7: Logger Setup
print("\n" + "="*60)
print("TEST 7: Logger Setup")
print("="*60)
try:
    from utils.logger import setup_logger
    setup_logger()
    print(f"✅ Logger setup successful")
    
    # Check if log file exists
    log_path = Path("logs/sgx_pipeline.log")
    if log_path.exists():
        print(f"✅ Log file exists: {log_path}")
        print(f"   Size: {log_path.stat().st_size} bytes")
    else:
        print(f"⚠️  Log file not yet created (will be created on first run)")
except Exception as e:
    print(f"❌ Logger error: {e}")

# Test 8: Download Directory
print("\n" + "="*60)
print("TEST 8: Download Directory")
print("="*60)
try:
    from pathlib import Path
    data_dir = Path("data/raw")
    if data_dir.exists():
        print(f"✅ Data directory exists: {data_dir}")
        subdirs = list(data_dir.iterdir())
        print(f"   Contains {len(subdirs)} subdirectories")
        if subdirs:
            for subdir in list(subdirs)[:3]:
                if subdir.is_dir():
                    print(f"   - {subdir.name}")
    else:
        print(f"❌ Data directory does not exist")
except Exception as e:
    print(f"❌ Directory error: {e}")

print("\n" + "="*60)
print("ENVIRONMENT TEST COMPLETE")
print("="*60 + "\n")
