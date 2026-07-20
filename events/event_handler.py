"""
Base Event Handler Interface

All event handlers inherit from this class.
Each handler decides if an announcement matches its event type.
"""

from abc import ABC, abstractmethod
from models.event import Event


class EventHandler(ABC):
    """Abstract base class for event handlers"""

    @abstractmethod
    def can_handle(self, announcement) -> bool:
        """
        Check if this handler can process the announcement.
        Each handler implements its own matching logic.
        """
        pass

    @abstractmethod
    def handle(self, announcement, document=None) -> Event:
        """
        Create an event from the announcement.
        Return None if this handler doesn't match.
        """
        pass
