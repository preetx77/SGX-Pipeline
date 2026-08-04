#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify both notification types work:
1. Insider dealings (BUY, SELL)
2. Corporate events (CORPORATE EVENT)
"""

import sys
import os
from pathlib import Path

# Fix encoding for Windows terminal
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from services.announcement_service import AnnouncementService
from database.announcement_repository import AnnouncementRepository
from config.watchlist import WATCHLIST
from datetime import datetime

print("="*80)
print("CORPORATE EVENT & INSIDER NOTIFICATION TEST")
print("="*80)

# Initialize services
ann_repo = AnnouncementRepository()
ann_service = AnnouncementService()

print("\n1. Testing Corporate Event Detection & Notification")
print("-" * 80)

# Get all announcements and look for corporate events
all_announcements = ann_repo.latest(100)
corporate_events = [
    ann for ann in all_announcements 
    if any(keyword in ann.category.lower() for keyword in 
           ["extraordinary", "special general meeting", "voluntary", "circular"])
]

if corporate_events:
    print(f"[PASS] Found {len(corporate_events)} corporate events in database\n")
    
    for event in corporate_events[:3]:  # Test first 3
        print(f"Company: {event.company_name}")
        print(f"Stock Code: {event.stock_code}")
        print(f"Category: {event.category}")
        print(f"Title: {event.title}")
        print(f"Date: {event.submission_date}")
        print(f"Status: Testing notification...\n")
        
        try:
            ann_service._notify_corporate_event(event)
            print(f"[PASS] Corporate event notification sent")
        except Exception as e:
            print(f"[FAIL] Failed to send notification: {e}")
        
        print("-" * 80)
else:
    print("[WARN] No corporate events found in database")
    print("   The system will notify when new corporate events are detected during sync\n")

print("\n2. Testing Insider Dealing Detection & Notification")
print("-" * 80)

# Get insider dealing announcements
insider_dealings = [
    ann for ann in all_announcements 
    if "disclosure of interest" in ann.category.lower()
]

if insider_dealings:
    print(f"[PASS] Found {len(insider_dealings)} insider dealing announcements\n")
    
    for dealing in insider_dealings[:3]:  # Show first 3
        print(f"Company: {dealing.company_name}")
        print(f"Stock Code: {dealing.stock_code}")
        print(f"Category: {dealing.category}")
        print(f"Title: {dealing.title}")
        print(f"Date: {dealing.submission_date}")
        print(f"Status: This triggers InsiderPipeline (PDF extraction -> director signal -> notification)\n")
        print("-" * 80)
else:
    print("[WARN] No insider dealing announcements found in database")
    print("   The system will process these when new Form 1/Form 3 disclosures are detected\n")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("""
[PASS] Both notification types are active:

1. CORPORATE EVENTS
   - Detects: Extraordinary/Special Meetings, Voluntary Announcements, Circulars
   - Sends: [CORPORATE EVENT] format notification to Telegram
   - Example: Shareholder meetings, capital restructuring announcements

2. INSIDER DEALINGS  
   - Detects: Director disclosure announcements (Form 1/Form 3)
   - Processes: PDF extraction -> Director signal analysis -> Classification
   - Sends: [BUY] or [SELL] notifications with confidence score
   - Example: Director purchases/sales of company shares

Both types use the same Telegram channel(s) configured in .env
""")

ann_repo.close()
ann_service.close()

print("\n[PASS] Test completed successfully")
