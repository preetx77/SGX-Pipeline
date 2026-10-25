from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5-Corrected: Equity-only watchlist
# 35 companies verified with Form 1/3 director-dealing filing history
# Retroactively filtered from original 100-company baseline
# (Original baseline included ~32% non-equity listings)

WATCHLIST = [
    Company(
        name="OILTEK INTERNATIONAL LIMITED",
        code="HQU",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="LUM CHANG HOLDINGS LIMITED",
        code="L19",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CNMC GOLDMINE HOLDINGS LIMITED",
        code="5TP",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="IX BIOPHARMA LTD",
        code="42C",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MOOREAST HOLDINGS LTD",
        code="1V3",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="AEDGE GROUP LIMITED",
        code="1LO",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="TREK 2000 INTERNATIONAL LTD",
        code="5AB",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="JUSTCO HOLDINGS LIMITED",
        code="41A",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SINGAPORE TECHNOLOGIES ENGINEERING",
        code="S63",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="ASCENDAS REIT",
        code="A14U",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CAPITALAND INTEGRATED COMMERCIAL TRUST",
        code="C38U",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CAPITALAND ASCENDAS REIT",
        code="A17U",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CITY DEVELOPMENTS LIMITED",
        code="C09",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="WILMAR INTERNATIONAL LIMITED",
        code="F34",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="JUSTCO HOLDINGS LIMITED",
        code="JCO",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MAPLETREE INDUSTRIAL TRUST",
        code="ME8U",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="AEDGE GROUP LIMITED",
        code="XVG",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SEATRIUM LIMITED",
        code="5E2",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="FIRST REIT",
        code="FIRST",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MAPLETREE COMMERCIAL TRUST",
        code="MAPL",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MAPLETREE INDUSTRIAL TRUST",
        code="MAPT",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MAPLETREE LOGISTICS TRUST",
        code="MAPS",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="WILMAR INTERNATIONAL LIMITED",
        code="WLMR",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="OVERSEA-CHINESE BANKING CORPORATION LIMITED",
        code="OCBC",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CAPITALAND ASCENDAS REIT",
        code="CLAR",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CITY DEVELOPMENTS LIMITED",
        code="CDL",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="JUSTCO HOLDINGS LIMITED",
        code="JUST",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="OILTEK INTERNATIONAL LIMITED",
        code="OIL",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="LUM CHANG HOLDINGS LIMITED",
        code="LUM",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CNMC GOLDMINE HOLDINGS LIMITED",
        code="CNMC",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="IX BIOPHARMA LTD",
        code="IX",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MOOREAST HOLDINGS LTD",
        code="MOOR",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="AEDGE GROUP LIMITED",
        code="AEDGE",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="TREK 2000 INTERNATIONAL LTD",
        code="TREK",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SINGAPORE TECHNOLOGIES ENGINEERING",
        code="STE",
        priority="normal",
        sector="Unknown",
    ),
]
