"""
Financial Results Event Handler

Detects announcements about financial statements and results.
"""

from datetime import datetime
from models.event import Event
from events.event_handler import EventHandler


class FinancialResultsHandler(EventHandler):

    KEYWORDS = [
        "financial statements",
        "financial statement",
        "interim financial",
        "results",
        "full yearly results",
        "half yearly results",
        "1h results",
        "2h results",
        "3q results"
    ]

    def can_handle(self, announcement) -> bool:
        """Check if announcement is about financial results"""
        category = announcement.category.lower()
        title = announcement.title.lower()
        
        for keyword in self.KEYWORDS:
            if keyword in category or keyword in title:
                return True
        
        return False

    def handle(self, announcement, document=None) -> Event:
        """Create a financial results event"""
        if not self.can_handle(announcement):
            return None

        return Event(
            event_type="FINANCIAL_RESULTS",
            announcement_id=announcement.announcement_id,
            company_name=announcement.company_name,
            stock_code=announcement.stock_code,
            title=announcement.title,
            timestamp=datetime.now(),
            payload={}
        )
