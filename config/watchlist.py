from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5+ Watchlist: 32 Verified Companies
# Baseline 34 - 2 dropped (U11, Z74, BN4, C8R, TQ5, N2IU, MCOB, K6S)
# + Phase 1 Expansion 6 - 1 dropped (K6S)
#
# All 32 entries verified by:
# - Direct SGX code lookup
# - Listing status active (not delisted)
# - Insider filing activity (24-month window, AnnouncementRouter.is_insider)
# - Minimum 1 insider announcement in measurement window
# 
# Companies dropped (zero insider filings in 24-month window):
# - U11 (UOB): 100 total announcements, 0 insider
# - Z74 (Singtel): 0 announcements returned
# - BN4 (Keppel): 0 announcements returned
# - C8R (Jiutian): 34 total, 0 insider
# - TQ5 (Frasers): 100 total, 0 insider
# - N2IU (Mapletree CT): 0 announcements returned
# - MCOB (Bangkok Bank): 30 total, 0 insider
# - K6S (Prudential): 100 total, 0 insider

WATCHLIST = [
    # BASELINE EQUITIES (26 verified)
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
    Company(name="SINGAPORE TECHNOLOGIES ENGINEERING", code="S63", priority="high", sector="Engineering"),
    Company(name="GENTING SINGAPORE LIMITED", code="G13", priority="normal", sector="Hospitality"),
    Company(name="CITY DEVELOPMENTS LIMITED", code="C09", priority="normal"),
    Company(name="GUOCOLAND LIMITED", code="F17", priority="normal"),
    Company(name="WILMAR INTERNATIONAL LIMITED", code="F34", priority="normal"),
    Company(name="SINGAPORE EXCHANGE LIMITED", code="S68", priority="normal"),
    Company(name="SIA ENGINEERING COMPANY LIMITED", code="S59", priority="normal"),
    Company(name="OVERSEA-CHINESE BANKING CORPORATION LIMITED", code="O39", priority="normal"),
    Company(name="SINGAPORE AIRLINES LIMITED", code="C6L", priority="normal"),
    Company(name="SEATRIUM LIMITED", code="5E2", priority="normal"),
    Company(name="CAPITALAND INVESTMENT LIMITED", code="9CI", priority="normal"),
    
    # BASELINE REITs/TRUSTS (6 verified)
    Company(name="CAPITALAND ASCENDAS REIT", code="A17U", priority="normal", sector="Real Estate"),
    Company(name="CAPITALAND INTEGRATED COMMERCIAL TRUST", code="C38U", priority="normal", sector="Real Estate"),
    Company(name="FIRST REIT", code="AW9U", priority="normal"),
    Company(name="MAPLETREE INDUSTRIAL TRUST", code="ME8U", priority="normal"),
    Company(name="MAPLETREE LOGISTICS TRUST", code="M44U", priority="normal"),
    
    # PHASE 1 EXPANSION (5 verified - K6S dropped for zero insider filings)
    Company(name="DBS GROUP HOLDINGS", code="D05", priority="high", sector="Banking"),
    Company(name="GREAT EASTERN HOLDINGS", code="G07", priority="high", sector="Insurance"),
    Company(name="HAW PAR CORPORATION", code="H02", priority="normal", sector="Consumer"),
    Company(name="JARDINE CYCLE & CARRIAGE", code="C07", priority="normal", sector="Consumer"),
    Company(name="VENTURE CORPORATION", code="V03", priority="normal", sector="Tech"),
]
