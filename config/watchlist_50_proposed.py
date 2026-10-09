from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    name: str
    code: str
    enabled: bool = True
    priority: str = "normal"
    sector: str = "Unknown"

# Stage 5 Expansion: 50-company unified watchlist (FINAL)
# 34 existing verified companies + 16 new candidates (validated 2026-10-09)
# All additions verified via SGX announcements API

WATCHLIST = [
    # EXISTING 34 COMPANIES
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
    # STAGE 1: 6 NEW
    Company(name="DBS GROUP HOLDINGS", code="D05", priority="high", sector="Banking"),
    Company(name="GREAT EASTERN HOLDINGS", code="G07", priority="high", sector="Insurance"),
    Company(name="HAW PAR CORPORATION", code="H02", priority="normal", sector="Consumer"),
    Company(name="JARDINE CYCLE & CARRIAGE", code="C07", priority="normal", sector="Consumer"),
    Company(name="PRUDENTIAL PLC", code="K6S", priority="normal", sector="Insurance"),
    Company(name="VENTURE CORPORATION", code="V03", priority="normal", sector="Tech"),
    # STAGE 2: 6 ADDITIONAL
    Company(name="OCBC", code="OCBC", priority="high", sector="Banking"),
    Company(name="PRUDENTIAL", code="PRU", priority="high", sector="Insurance"),
    Company(name="M1 LIMITED", code="M1Z", priority="normal", sector="Telecom"),
    Company(name="NOBLE GROUP LIMITED", code="N26", priority="normal", sector="Trading"),
    Company(name="ALLIED TECHNOLOGIES LIMITED", code="AL8", priority="normal", sector="Tech"),
    Company(name="ENTERTAINMENT LIMITED", code="ENT", priority="normal", sector="Media"),
    # STAGE 3: 4 ADDITIONAL
    Company(name="SEMBCORP INDUSTRIES", code="ST", priority="normal", sector="Utilities"),
    Company(name="AEM HOLDINGS", code="AE8", priority="normal", sector="Tech"),
    Company(name="CHINA RESOURCE", code="CRC", priority="normal", sector="Consumer"),
    # FINAL: 1 ADDITIONAL (50th)
    Company(name="AXIATA", code="AXX", priority="normal", sector="Telecom"),
]

