from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class InsiderSignal:

    announcement_id: str

    company_name: str

    stock_code: str

    director_name: str

    signal: bool

    signal_type: str

    direction: str

    importance: int

    confidence: float

    reason: str

    transaction_type: str

    shares: int | None = None

    price: float | None = None

    value: float | None = None

    direct_interest_before: int | None = None

    direct_interest_after: int | None = None

    decision: str = "IGNORE"

    market_impact: str = "Neutral"

    summary: str = ""

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())