from dataclasses import dataclass


@dataclass(slots=True)
class FinancialMetric:

    announcement_id: str

    company_name: str

    stock_code: str

    metric_name: str

    current_value: float

    previous_value: float | None = None

    currency: str | None = None

    unit: str | None = None

    reporting_period: str | None = None

    def change(self):

        if self.previous_value is None:
            return None

        if self.previous_value == 0:
            return None

        return (
            (self.current_value-self.previous_value)
            / self.previous_value
        ) * 100

    def __str__(self):

        return f"{self.metric_name}: {self.current_value}"