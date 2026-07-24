from enum import Enum
from dataclasses import dataclass

from core.event_type import EventType
from core.priority import get_priority, Priority


@dataclass(frozen=True)
class Classification:
    event_type: EventType
    reason: str
    priority: Priority


def classify(announcement) -> Classification:
    """
    Classify an SGX announcement using deterministic rules.
    """

    category = (announcement.category or "").lower()
    title = (announcement.title or "").lower()

    # ----------------------------
    # Insider Dealings
    # ----------------------------
    if (
        "disclosure of interest" in category
        or "changes in interest" in title
        or "change in interest" in title
    ):
        event = EventType.INSIDER

        return Classification(
            event_type=event,
            reason="Matched disclosure of interest keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # Financial Results
    # ----------------------------
    if (
        "financial statements" in category
        or "results release" in title
        or "quarterly" in title
        or "half year" in title
        or "full year" in title
    ):
        event = EventType.RESULTS

        return Classification(
            event_type=event,
            reason="Matched financial reporting keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # Trading Halt
    # ----------------------------
    if (
        "trading halt" in category
        or "request for trading halt" in title
    ):
        event = EventType.HALT

        return Classification(
            event_type=event,
            reason="Matched trading halt keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # Acquisition / Disposal
    # ----------------------------
    if (
        "asset acquisitions" in category
        or "asset disposals" in category
        or "acquisition" in title
        or "disposal" in title
    ):
        event = EventType.ACQUISITION

        return Classification(
            event_type=event,
            reason="Matched acquisition/disposal keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # Share Buyback
    # ----------------------------
    if (
        "buy back" in category
        or "buy-back" in title
        or "share buy back" in title
    ):
        event = EventType.BUYBACK

        return Classification(
            event_type=event,
            reason="Matched buyback keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # Rights Issue
    # ----------------------------
    if (
        "rights issue" in title
        or "rights" in category
    ):
        event = EventType.RIGHTS

        return Classification(
            event_type=event,
            reason="Matched rights issue keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # Dividend
    # ----------------------------
    if (
        "dividend" in title
        or "dividend" in category
    ):
        event = EventType.DIVIDEND

        return Classification(
            event_type=event,
            reason="Matched dividend keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # AGM
    # ----------------------------
    if (
        "annual general meeting" in title
        or "agm" in title
        or "general meeting" in category
    ):
        event = EventType.AGM

        return Classification(
            event_type=event,
            reason="Matched AGM keywords.",
            priority=get_priority(event),
        )

    # ----------------------------
    # Board Changes
    # ----------------------------
    if (
        "appointment" in title
        or "cessation" in title
        or "director" in category
    ):
        event = EventType.BOARD

        return Classification(
            event_type=event,
            reason="Matched board appointment keywords.",
            priority=get_priority(event),
        )

    event = EventType.GENERAL

    return Classification(
        event_type=event,
        reason="No classification rule matched.",
        priority=get_priority(event),
    )