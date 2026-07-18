"""
Event Engine - Registry-Based Handler Pattern

The engine maintains a list of handlers.
Each handler is responsible for its own event type detection.
Adding new event types requires only a new handler class.
The engine itself never changes.

Returns a LIST of events (not single event) to support:
- One announcement generating multiple events
- Example: Annual Report → FinancialResultsEvent + DividendEvent
"""

from services.handlers import (
    DirectorDealingsHandler,
    FinancialResultsHandler,
    DividendHandler
)


class EventEngine:
    """
    Generic Event Engine using registry pattern.
    
    Handlers are registered in __init__.
    The process() method loops through handlers and collects ALL matching events.
    Returns a list of events (may be empty, single, or multiple).
    """

    def __init__(self):
        """Initialize with all available handlers"""
        self.handlers = [
            DirectorDealingsHandler(),
            FinancialResultsHandler(),
            DividendHandler(),
        ]

    def process(self, announcement):
        """
        Process an announcement through all registered handlers.
        
        Returns a list of ALL matching events.
        One announcement can generate multiple events.
        
        Example:
            Annual Report could trigger:
              - FinancialResultsEvent
              - DividendEvent
              - InvestorPresentationEvent
        """
        events = []
        
        for handler in self.handlers:
            if handler.can_handle(announcement):
                event = handler.handle(announcement)
                if event:
                    events.append(event)
        
        return events

    def register_handler(self, handler):
        """
        Register a new handler at runtime.
        
        Usage: engine.register_handler(MyCustomHandler())
        """
        self.handlers.append(handler)
