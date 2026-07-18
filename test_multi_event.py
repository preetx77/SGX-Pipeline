"""
Test demonstrating multiple events from one announcement.

This shows why returning a list is important.
An announcement can match multiple handlers and generate multiple events.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.announcement_repository import AnnouncementRepository
from services.event_engine import EventEngine

repo = AnnouncementRepository()
engine = EventEngine()

# Find announcements that generate multiple events
announcements = repo.latest(100)

print("=" * 80)
print("MULTI-EVENT ANNOUNCEMENTS")
print("=" * 80)

multi_event_count = 0

for announcement in announcements:
    events = engine.process(announcement)
    
    # Look for announcements with 2+ events
    if len(events) > 1:
        multi_event_count += 1
        print(f"\n{announcement.title}")
        print(f"Generated {len(events)} events:")
        for event in events:
            print(f"  - {event.event_type}")
        
        if multi_event_count >= 5:
            break

if multi_event_count == 0:
    print("\nNo multi-event announcements found in this batch.")
    print("This shows the potential: when keywords overlap,")
    print("one announcement can trigger multiple handlers.")
    print("\nExample scenario:")
    print("  Annual Report announcement with dividend")
    print("  → FinancialResultsEvent + DividendEvent")

repo.close()
