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

    Company(
        name="HYPHENS PHARMA INTERNATIONAL LIMITED",
        code="1J5",
        priority="high",
        sector="Healthcare",
    ),

    Company(
        name="LUM CHANG HOLDINGS LIMITED",
        code="L19",
        priority="normal",
        sector="Construction",
    ),

    Company(
        name="CREATIONS FOOD COMPANY LIMITED",
        code="5FO",
        priority="normal",
        sector="Consumer",
    ),

    Company(
        name="CNMC GOLDMINE HOLDINGS LIMITED",
        code="5TP",
        priority="high",
        sector="Mining",
    ),

    Company(
        name="GRAND BANKS YACHTS LIMITED",
        code="G50",
        priority="normal",
        sector="Marine",
    ),

    Company(
        name="IX BIOPHARMA LTD",
        code="42C",
        priority="high",
        sector="Biotechnology",
    ),

    Company(
        name="MOOREAST HOLDINGS LTD",
        code="1V3",
        priority="normal",
        sector="Marine",
    ),

    Company(
        name="AEDGE GROUP LIMITED",
        code="1LO",
        priority="normal",
        sector="Technology",
    ),

    Company(
        name="OLAM GROUP LIMITED",
        code="VC2",
        priority="high",
        sector="Agribusiness",
    ),

    Company(
        name="TREK 2000 INTERNATIONAL LTD",
        code="5AB",
        priority="normal",
        sector="Technology",
    ),

    Company(
        name="JUSTCO HOLDINGS LIMITED",
        code="41A",
        priority="normal",
        sector="Real Estate",
    ),

]
 
WATCHLIST_CODES = {
    company.code
    for company in WATCHLIST
    if company.enabled
}