import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.announcement_repository import AnnouncementRepository

from services.event_engine import EventEngine

from notifications.console_notifier import ConsoleNotifier


repo = AnnouncementRepository()

engine = EventEngine()

notifier = ConsoleNotifier()


announcements = repo.latest(20)

for announcement in announcements:

    # process() now returns a LIST of events
    events = engine.process(announcement)
    
    # Handle multiple events per announcement
    for event in events:
        notifier.notify(event)

repo.close()
