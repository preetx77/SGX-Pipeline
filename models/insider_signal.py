from dataclasses import dataclass


@dataclass
class InsiderSignal:
    """
    Final intelligence generated from a DirectorDealing.

    This is the object consumed by notifiers,
    dashboards and future ranking engines.
    """

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

    decision: str = "IGNORE"

    market_impact: str = "Neutral"

    summary: str = ""