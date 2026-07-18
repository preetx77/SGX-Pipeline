"""
Dividend Event Handler

Detects announcements about dividend payments.
"""

from datetime import datetime
from models.event import Event
from services.event_handler import EventHandler


class DividendHandler(EventHandler):

    KEYWORDS = [
        "dividend",
        "cash dividend",
        "distribution",
        "bonus",
        "capital return"
    ]

    def can_handle(self, announcement) -> bool:
        """Check if announcement is about dividend"""
        category = announcement.category.lower()
        title = announcement.title.lower()
        
        for keyword in self.KEYWORDS:
            if keyword in category or keyword in title:
                return True
        
        return False

    def handle(self, announcement) -> Event:
        """Create a dividend event"""
        if not self.can_handle(announcement):
            return None

        return Event(
            event_type="DIVIDEND",
            announcement_id=announcement.announcement_id,
            company_name=announcement.company_name,
            stock_code=announcement.stock_code,
            title=announcement.title,
            timestamp=datetime.now(),
            payload={}
        )
