"""
Event Engine - Registry-Based Handler Pattern

The engine maintains a list of handlers.
Each handler is responsible for its own event type detection.
Adding new event types requires only a new handler class.
The engine itself never changes.

Returns a LIST of events (not single event) to support:
- One announcement generating multiple events
- Example: Annual Report -> FinancialResultsEvent + DividendEvent
"""

from events.handlers import (
    DirectorDealingsHandler,
    FinancialResultsHandler,
    DividendHandler
)

from database.document_repository import DocumentRepository


class EventEngine:
    """
    Generic Event Engine using registry pattern.

    Handlers are registered in __init__.
    The process() method loops through handlers and collects ALL matching events.
    Returns a list of events (may be empty, single, or multiple).
    """

    def __init__(self):
        """Initialize handlers and repositories"""

        self.handlers = [
            DirectorDealingsHandler(),
            FinancialResultsHandler(),
            DividendHandler(),
        ]

        # Repository used to fetch documents associated
        # with an announcement.
        self.document_repository = DocumentRepository()

    def process(self, announcement):
        """
        Process one announcement.

        Flow:

            Announcement
                  │
                  ▼
          Find associated document
                  │
                  ▼
             Registered Handlers
                  │
                  ▼
            List of Event objects
        """

        events = []

        # Fetch documents belonging to this announcement
        documents = self.document_repository.get_documents_by_announcement(
            announcement.announcement_id
        )

        # Most announcements currently have one primary document.
        document = documents[0] if documents else None

        # Pass both announcement and document
        # to every registered handler.
        for handler in self.handlers:

            if not handler.can_handle(announcement):
                continue

            event = handler.handle(
                announcement,
                document
            )

            if event is not None:
                events.append(event)

        return events

    def register_handler(self, handler):
        """
        Register a new handler.

        Example:
            engine.register_handler(MyCustomHandler())
        """

        self.handlers.append(handler)