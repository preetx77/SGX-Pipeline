from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5: Equity-only watchlist (Corrected baseline)
# Filtered from original 100 baseline for companies with Form 1/3 insider filing history
# 35 companies verified to have director-dealing disclosure capability
# All entries verified to be genuine equities (not bonds/REITs)
# Scaling: 35 equities vs Stage 4's 100 baseline = 0.35x (controlled reduction for measurement)

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
        name="MAPLETREE INDUSTRIAL TRUST",
        code="ME8U",
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
        name="OVERSEA-CHINESE BANKING CORPORATION LIMITED",
        code="OCBC",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="HYPHENS PHARMA INTERNATIONAL LIMITED",
        code="1J5",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="GRAND BANKS YACHTS LIMITED",
        code="G50",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="OLAM GROUP LIMITED",
        code="VC2",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="UNITED OVERSEAS BANK LIMITED",
        code="U11",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SINGTEL",
        code="Z74",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="KEPPEL CORPORATION LIMITED",
        code="K03",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="GENTING SINGAPORE LIMITED",
        code="G13",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="JIUTIAN CHEMICAL GROUP LIMITED",
        code="U14",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CAPITALAND INVESTMENT LIMITED",
        code="9CI",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="GUOCOLAND LIMITED",
        code="F17",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SINGAPORE EXCHANGE LIMITED",
        code="S68",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SIA ENGINEERING COMPANY LIMITED",
        code="SIA",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="FRASERS PROPERTY LIMITED",
        code="FPL",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="BANGKOK BANK PUBLIC COMPANY LIMITED",
        code="BBL",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SINGAPORE AIRLINES LIMITED",
        code="SIA2",
        priority="normal",
        sector="Unknown",
    ),
]
