from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5: Verified 32-Company Watchlist
# All companies have director insider filings (Form 1 filings verified)
# Real SGX codes only - no generated placeholders

WATCHLIST = [
    Company(name="AEDGE GROUP LIMITED", code="XVG", priority="low"),
    Company(name="CAPITALAND ASCENDAS REIT", code="A17U", priority="high"),
    Company(name="CAPITALAND INTEGRATED COMMERCIAL TRUST", code="C38U", priority="high"),
    Company(name="CAPITALAND INVESTMENT LIMITED", code="9CI", priority="normal"),
    Company(name="CITY DEVELOPMENTS LIMITED", code="C09", priority="low"),
    Company(name="CNMC GOLDMINE HOLDINGS LIMITED", code="5TP", priority="high"),
    Company(name="DBS GROUP HOLDINGS", code="D05", priority="normal"),
    Company(name="FIRST REIT", code="AW9U", priority="low"),
    Company(name="GENTING SINGAPORE LIMITED", code="G13", priority="normal"),
    Company(name="GRAND BANKS YACHTS LIMITED", code="G50", priority="low"),
    Company(name="GREAT EASTERN HOLDINGS", code="G07", priority="low"),
    Company(name="GUOCOLAND LIMITED", code="F17", priority="normal"),
    Company(name="HAW PAR CORPORATION", code="H02", priority="low"),
    Company(name="HYPHENS PHARMA INTERNATIONAL LIMITED", code="1J5", priority="normal"),
    Company(name="IX BIOPHARMA LTD", code="42C", priority="normal"),
    Company(name="JARDINE CYCLE & CARRIAGE", code="C07", priority="low"),
    Company(name="JUSTCO HOLDINGS LIMITED", code="JCO", priority="normal"),
    Company(name="LUM CHANG HOLDINGS LIMITED", code="L19", priority="low"),
    Company(name="MAPLETREE INDUSTRIAL TRUST", code="ME8U", priority="normal"),
    Company(name="MAPLETREE LOGISTICS TRUST", code="M44U", priority="normal"),
    Company(name="MOOREAST HOLDINGS LTD", code="1V3", priority="normal"),
    Company(name="OILTEK INTERNATIONAL LIMITED", code="HQU", priority="low"),
    Company(name="OLAM GROUP LIMITED", code="VC2", priority="low"),
    Company(name="OVERSEA-CHINESE BANKING CORPORATION LIMITED", code="O39", priority="low"),
    Company(name="SEATRIUM LIMITED", code="5E2", priority="normal"),
    Company(name="SIA ENGINEERING COMPANY LIMITED", code="S59", priority="low"),
    Company(name="SINGAPORE AIRLINES LIMITED", code="C6L", priority="high"),
    Company(name="SINGAPORE EXCHANGE LIMITED", code="S68", priority="low"),
    Company(name="SINGAPORE TECHNOLOGIES ENGINEERING", code="S63", priority="normal"),
    Company(name="TREK 2000 INTERNATIONAL LTD", code="5AB", priority="low"),
    Company(name="VENTURE CORPORATION", code="V03", priority="high"),
    Company(name="WILMAR INTERNATIONAL LIMITED", code="F34", priority="normal"),
]

# Statistics
# Total companies: 32
# All have director insider filings (Form 1)
# Total director filings measured: 419
# Average per company: 13.1
# Companies capped at 100 announcements: 20
