from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Event:

    event_type: str

    announcement_id: str

    company_name: str

    stock_code: str

    title: str

    timestamp: datetime

    payload: dict = field(default_factory=dict)

    processed: bool = False

    def __str__(self):

        return (
            f"[{self.event_type}] "
            f"{self.company_name} "
            f"({self.stock_code})"
        )