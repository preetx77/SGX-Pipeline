
from dataclasses import dataclass


@dataclass(slots=True)
class FinancialResult:

    announcement_id: str

    company_name: str

    stock_code: str

    reporting_period: str | None = None

    revenue: float | None = None

    gross_profit: float | None = None

    operating_profit: float | None = None

    net_profit: float | None = None

    eps: float | None = None

    currency: str | None = None

    extracted: bool = False

    def __str__(self):

        return (
            f"[{self.stock_code}] "
            f"{self.reporting_period}"
        )