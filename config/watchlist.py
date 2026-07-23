from dataclasses import dataclass


@dataclass(frozen=True)
class Company:

    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"


WATCHLIST = [

    Company(
        name="OILTEK INTERNATIONAL LIMITED",
        code="HQU",
        priority="high",
        sector="Industrial",
    ),

]

WATCHLIST_CODES = {
    company.code
    for company in WATCHLIST
    if company.enabled
}