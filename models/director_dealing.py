from dataclasses import dataclass


@dataclass
class DirectorDealing:

    announcement_id: str

    company_name: str

    stock_code: str

    director_name: str | None = None

    dealing_date: str | None = None

    action: str | None = None

    transaction_type: str | None = None

    shares: int | None = None

    price: float | None = None

    value: float | None = None

    currency: str | None = None

    interest_type: str | None = None

    direct_before: int | None = None

    direct_after: int | None = None

    deemed_before: int | None = None

    deemed_after: int | None = None

    signal_strength: int | None = None

    notes: str | None = None

    transaction_type: str | None = None

    importance: int | None = None

    direct_interest_before: int | None = None

    direct_interest_after: int | None = None

    deemed_interest_before: int | None = None

    deemed_interest_after: int | None = None