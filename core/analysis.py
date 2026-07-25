from dataclasses import dataclass
from typing import Optional

from core.classifier import Classification


@dataclass(slots=True)
class AnnouncementAnalysis:
    """
    Intelligence generated from an announcement.

    The Announcement object always stays as the raw SGX payload.
    Everything we infer lives here.
    """

    classification: Classification

    insider_event: Optional[object] = None

    ai_summary: Optional[str] = None

    narrative_score: Optional[float] = None

    sentiment: Optional[str] = None