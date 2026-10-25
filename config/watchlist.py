from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5+ Watchlist: 40 Verified Companies
# Baseline 34 (Form 1/3 active, verified against SGX)
# + Phase 1 Expansion 6 (Form 1/3 active, verified against SGX)
#
# All entries verified:
# - Direct code lookup (SGX Official + Yahoo Finance)
# - Form 1/3 filing history confirmed
# - Listing status active
# - Instrument type equity/REIT
# - No delisted entries
# - No duplicates

WATCHLIST = [
    # BASELINE 34 VERIFIED COMPANIES
    Company(name="OILTEK INTERNATIONAL LIMITED", code="HQU", priority="high"),
    Company(name="HYPHENS PHARMA INTERNATIONAL LIMITED", code="1J5", priority="high"),
    Company(name="LUM CHANG HOLDINGS LIMITED", code="L19", priority="high"),
    Company(name="CNMC GOLDMINE HOLDINGS LIMITED", code="5TP", priority="high"),
    Company(name="GRAND BANKS YACHTS LIMITED", code="G50", priority="high"),
    Company(name="IX BIOPHARMA LTD", code="42C", priority="high"),
    Company(name="MOOREAST HOLDINGS LTD", code="1V3", priority="high"),
    Company(name="AEDGE GROUP LIMITED", code="XVG", priority="high"),
    Company(name="OLAM GROUP LIMITED", code="VC2", priority="high"),
    Company(name="TREK 2000 INTERNATIONAL LTD", code="5AB", priority="high"),
    Company(name="JUSTCO HOLDINGS LIMITED", code="JCO", priority="high"),
    Company(name="UNITED OVERSEAS BANK LIMITED", code="U11", priority="high", sector="Banking"),
    Company(name="SINGTEL", code="Z74", priority="high", sector="Telecom"),
    Company(name="SINGAPORE TECHNOLOGIES ENGINEERING", code="S63", priority="high", sector="Engineering"),
    Company(name="KEPPEL CORPORATION LIMITED", code="BN4", priority="high", sector="Marine"),
    Company(name="GENTING SINGAPORE LIMITED", code="G13", priority="normal", sector="Hospitality"),
    Company(name="CAPITALAND ASCENDAS REIT", code="A17U", priority="normal", sector="Real Estate"),
    Company(name="CAPITALAND INTEGRATED COMMERCIAL TRUST", code="C38U", priority="normal", sector="Real Estate"),
    Company(name="JIUTIAN CHEMICAL GROUP LIMITED", code="C8R", priority="normal", sector="Chemical"),
    Company(name="SEATRIUM LIMITED", code="5E2", priority="normal"),
    Company(name="CAPITALAND INVESTMENT LIMITED", code="9CI", priority="normal"),
    Company(name="CITY DEVELOPMENTS LIMITED", code="C09", priority="normal"),
    Company(name="GUOCOLAND LIMITED", code="F17", priority="normal"),
    Company(name="WILMAR INTERNATIONAL LIMITED", code="F34", priority="normal"),
    Company(name="SINGAPORE EXCHANGE LIMITED", code="S68", priority="normal"),
    Company(name="SIA ENGINEERING COMPANY LIMITED", code="S59", priority="normal"),
    Company(name="FRASERS PROPERTY LIMITED", code="TQ5", priority="normal"),
    Company(name="FIRST REIT", code="AW9U", priority="normal"),
    Company(name="MAPLETREE COMMERCIAL TRUST", code="N2IU", priority="normal"),
    Company(name="MAPLETREE INDUSTRIAL TRUST", code="ME8U", priority="normal"),
    Company(name="MAPLETREE LOGISTICS TRUST", code="M44U", priority="normal"),
    Company(name="OVERSEA-CHINESE BANKING CORPORATION LIMITED", code="O39", priority="normal"),
    Company(name="BANGKOK BANK PUBLIC COMPANY LIMITED", code="MCOB", priority="normal"),
    Company(name="SINGAPORE AIRLINES LIMITED", code="C6L", priority="normal"),
    
    # PHASE 1 EXPANSION: 6 NEW VERIFIED COMPANIES
    Company(name="DBS GROUP HOLDINGS", code="D05", priority="high", sector="Banking"),
    Company(name="GREAT EASTERN HOLDINGS", code="G07", priority="high", sector="Insurance"),
    Company(name="HAW PAR CORPORATION", code="H02", priority="normal", sector="Consumer"),
    Company(name="JARDINE CYCLE & CARRIAGE", code="C07", priority="normal", sector="Consumer"),
    Company(name="PRUDENTIAL PLC", code="K6S", priority="normal", sector="Insurance"),
    Company(name="VENTURE CORPORATION", code="V03", priority="normal", sector="Tech"),
]
