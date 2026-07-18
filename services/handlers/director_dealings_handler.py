"""
Director Dealings Event Handler

Detects announcements about director share dealings.
"""

from datetime import datetime
from models.event import Event
from services.event_handler import EventHandler


class DirectorDealingsHandler(EventHandler):

    KEYWORDS = [
        "director dealings",
        "director's interest",
        "director interest",
        "disclosure of interest",
        "changes in interest",
        "ceasing to be a substantial shareholder",
        "becoming a substantial shareholder"
    ]

    def can_handle(self, announcement) -> bool:
        """Check if announcement is about director dealings"""
        category = announcement.category.lower()
        title = announcement.title.lower()
        
        for keyword in self.KEYWORDS:
            if keyword in category or keyword in title:
                return True
        
        return False

    def handle(self, announcement) -> Event:
        """Create a director dealings event"""
        if not self.can_handle(announcement):
            return None

        return Event(
            event_type="DIRECTOR_DEALINGS",
            announcement_id=announcement.announcement_id,
            company_name=announcement.company_name,
            stock_code=announcement.stock_code,
            title=announcement.title,
            timestamp=datetime.now(),
            payload={}
        )
