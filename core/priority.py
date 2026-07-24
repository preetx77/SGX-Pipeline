from dataclasses import dataclass

from core.event_type import EventType


@dataclass(frozen=True)
class Priority:
    score: int
    label: str
    stars: str
    notify: bool


_PRIORITY_MAP = {
    EventType.HALT: Priority(
        score=5,
        label="CRITICAL",
        stars="★★★★★",
        notify=True,
    ),

    EventType.RESULTS: Priority(
        score=5,
        label="CRITICAL",
        stars="★★★★★",
        notify=True,
    ),

    EventType.INSIDER: Priority(
        score=4,
        label="HIGH",
        stars="★★★★☆",
        notify=True,
    ),

    EventType.ACQUISITION: Priority(
        score=4,
        label="HIGH",
        stars="★★★★☆",
        notify=True,
    ),

    EventType.RIGHTS: Priority(
        score=4,
        label="HIGH",
        stars="★★★★☆",
        notify=True,
    ),

    EventType.DIVIDEND: Priority(
        score=3,
        label="MEDIUM",
        stars="★★★☆☆",
        notify=True,
    ),

    EventType.BOARD: Priority(
        score=3,
        label="MEDIUM",
        stars="★★★☆☆",
        notify=True,
    ),

    EventType.BUYBACK: Priority(
        score=2,
        label="LOW",
        stars="★★☆☆☆",
        notify=False,
    ),

    EventType.AGM: Priority(
        score=1,
        label="LOW",
        stars="★☆☆☆☆",
        notify=False,
    ),

    EventType.GENERAL: Priority(
        score=1,
        label="LOW",
        stars="★☆☆☆☆",
        notify=False,
    ),

    EventType.UNKNOWN: Priority(
        score=1,
        label="LOW",
        stars="★☆☆☆☆",
        notify=False,
    ),
}


def get_priority(event_type: EventType) -> Priority:
    """
    Returns priority information for an event type.
    """

    return _PRIORITY_MAP.get(
        event_type,
        _PRIORITY_MAP[EventType.UNKNOWN]
    )