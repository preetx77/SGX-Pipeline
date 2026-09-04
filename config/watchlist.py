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
        sector="Unknown",
    ),
    Company(
        name="HYPHENS PHARMA INTERNATIONAL LIMITED",
        code="1J5",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="LUM CHANG HOLDINGS LIMITED",
        code="L19",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="CREATIONS FOOD COMPANY LIMITED",
        code="5FO",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="CNMC GOLDMINE HOLDINGS LIMITED",
        code="5TP",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="GRAND BANKS YACHTS LIMITED",
        code="G50",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="IX BIOPHARMA LTD",
        code="42C",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="MOOREAST HOLDINGS LTD",
        code="1V3",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="AEDGE GROUP LIMITED",
        code="1LO",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="OLAM GROUP LIMITED",
        code="VC2",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="TREK 2000 INTERNATIONAL LTD",
        code="5AB",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="JUSTCO HOLDINGS LIMITED",
        code="41A",
        priority="high",
        sector="Unknown",
    ),

    # Stage 2 expansion: 13 new companies (25 total)
    Company(
        name="DBS GROUP HOLDINGS LIMITED",
        code="D05",
        priority="high",
        sector="Banking",
    ),
    Company(
        name="UNITED OVERSEAS BANK LIMITED",
        code="U11",
        priority="high",
        sector="Banking",
    ),
    Company(
        name="SINGTEL",
        code="Z74",
        priority="high",
        sector="Telecom",
    ),
    Company(
        name="SINGAPORE TECHNOLOGIES ENGINEERING",
        code="S63",
        priority="high",
        sector="Engineering",
    ),
    Company(
        name="KEPPEL CORPORATION LIMITED",
        code="K03",
        priority="high",
        sector="Marine",
    ),
    Company(
        name="GENTING SINGAPORE LIMITED",
        code="G13",
        priority="normal",
        sector="Hospitality",
    ),
    Company(
        name="ASCENDAS REIT",
        code="A14U",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="CAPITALAND INTEGRATED COMMERCIAL TRUST",
        code="C38U",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="JIUTIAN CHEMICAL GROUP LIMITED",
        code="U14",
        priority="normal",
        sector="Chemical",
    ),
    Company(
        name="CHINA PHARMA HOLDINGS INC",
        code="CPHI",
        priority="normal",
        sector="Healthcare",
    ),
    Company(
        name="CHINA SOS LIMITED",
        code="CHL",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="CHINA XD PLASTICS",
        code="CXDC",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="AEM HOLDINGS LIMITED",
        code="AWX",
        priority="normal",
        sector="Electronics",
    ),
]
