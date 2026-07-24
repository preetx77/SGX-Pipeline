from enum import Enum


class EventType(Enum):
    INSIDER = "Insider Dealings"
    RESULTS = "Financial Results"
    HALT = "Trading Halt"
    ACQUISITION = "Acquisition"
    BUYBACK = "Share Buyback"
    RIGHTS = "Rights Issue"
    DIVIDEND = "Dividend"
    AGM = "Annual General Meeting"
    BOARD = "Board Changes"
    GENERAL = "General Announcement"
    UNKNOWN = "Unknown"
