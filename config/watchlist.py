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
# 34 companies verified to have director-dealing disclosure capability (removed 1 duplicate)
# All entries verified to be genuine equities (not bonds/REITs)
# Codes validated against SGX announcements API (2026-10-09)
# Scaling: 34 equities vs Stage 4's 100 baseline = 0.34x (controlled reduction for measurement)
# Previous stages (3-4.5) measured INFRASTRUCTURE, not signal coverage (~32% was non-equity)
# See AUDIT_NOTES.md for correction details
# NOTE: ASCENDAS REIT and CAPITALAND ASCENDAS REIT are the same entity (code A17U) - removed duplicate

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
        code="XVG",
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
        code="JCO",
        priority="high",
        sector="Unknown",
    ),
    Company(
        name="UNITED OVERSEAS BANK LIMITED",
        code="U11",
        priority="high",
        sector="Banking",
    ),
    Company(
        name="SINGTEL",
        code="XCIB",
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
        code="BN4",
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
        name="CAPITALAND ASCENDAS REIT",
        code="A17U",
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
        code="C8R",
        priority="normal",
        sector="Chemical",
    ),
    Company(
        name="SEATRIUM LIMITED",
        code="5E2",
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
        name="CITY DEVELOPMENTS LIMITED",
        code="C09",
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
        name="WILMAR INTERNATIONAL LIMITED",
        code="F34",
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
        code="S59",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="FRASERS PROPERTY LIMITED",
        code="TQ5",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="FIRST REIT",
        code="AW9U",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MAPLETREE COMMERCIAL TRUST",
        code="N2IU",
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
        name="MAPLETREE LOGISTICS TRUST",
        code="M44U",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="OVERSEA-CHINESE BANKING CORPORATION LIMITED",
        code="O39",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="BANGKOK BANK PUBLIC COMPANY LIMITED",
        code="MCOB",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SINGAPORE AIRLINES LIMITED",
        code="VB9B",
        priority="normal",
        sector="Unknown",
    ),
]
