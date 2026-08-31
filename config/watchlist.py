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
        name="ASCENDAS REAL ESTATE INVESTMENT TRUST",
        code="A14",
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
        name="CapitaLand Investment Limited",
        code="CCIL",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="Keppel Corporation Limited",
        code="BN4",
        priority="high",
        sector="Energy",
    ),
    Company(
        name="Sembcorp Industries Limited",
        code="U96",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="Wilmar International Limited",
        code="WSH",
        priority="normal",
        sector="Agribusiness",
    ),
    Company(
        name="Thai Beverage Public Company Limited",
        code="Y92",
        priority="normal",
        sector="Consumer",
    ),
    Company(
        name="Singapore Airlines Limited",
        code="C6L",
        priority="high",
        sector="Aviation",
    ),
    Company(
        name="City Developments Limited",
        code="CIT",
        priority="normal",
        sector="Property",
    ),

    # Stage 2 expansion: 26 new companies
    Company(
        name="MERCURY TECHNOLOGY SOLUTIONS LIMITED",
        code="MERC",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="METRO INC",
        code="MR",
        priority="normal",
        sector="Logistics",
    ),
    Company(
        name="MARIGOLD MILLING LIMITED",
        code="MG",
        priority="normal",
        sector="Food",
    ),
    Company(
        name="MUAR RUBBER EXPORT ASSOCIATION",
        code="MREB",
        priority="normal",
        sector="Agriculture",
    ),
    Company(
        name="GENTING MALAYSIA BERHAD",
        code="GM",
        priority="normal",
        sector="Entertainment",
    ),
    Company(
        name="GENTING SINGAPORE LIMITED",
        code="G13",
        priority="normal",
        sector="Entertainment",
    ),
    Company(
        name="AEM HOLDINGS LIMITED",
        code="AWX",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="ASCOTRANS CAPITAL LIMITED",
        code="ASC",
        priority="normal",
        sector="Logistics",
    ),
    Company(
        name="PETROGRESS CORPORATION",
        code="PGR",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="ENDEAVOUR MINING CORPORATION",
        code="EDV",
        priority="normal",
        sector="Mining",
    ),
    Company(
        name="FRESNILLO PLC",
        code="FRES",
        priority="normal",
        sector="Mining",
    ),
    Company(
        name="SANVADA GLOBAL LIMITED",
        code="SVG",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="SEATRIUM PLC",
        code="SMR",
        priority="normal",
        sector="Mining",
    ),
    Company(
        name="POWERTECH TECHNOLOGY CORP LIMITED",
        code="PTCL",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="HSTECH INVESTMENT LIMITED",
        code="HSTECH",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="JIUTIAN CHEMICAL GROUP LIMITED",
        code="J99",
        priority="normal",
        sector="Chemical",
    ),
    Company(
        name="CAPITALAND PROPERTIES LIMITED",
        code="CLAND",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="NETLINK NBN TRUST",
        code="NBNSP",
        priority="normal",
        sector="Telecom",
    ),
    Company(
        name="MAPLETREE PAN ASIA COMMERCIAL TRUST",
        code="MPACT",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="MAPLETREE INDUSTRIAL TRUST",
        code="MINT",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="FRASERS LOGISTICS & INDUSTRIAL TRUST",
        code="CRCT",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="LIPPO MALLS INDONESIA RETAIL TRUST",
        code="LMRT",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="HUTCHINSON PORT HOLDINGS TRUST",
        code="HPHT",
        priority="normal",
        sector="Logistics",
    ),
    Company(
        name="STARBIZ TECHNOLOGY LIMITED",
        code="Z74C",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="GUOCOLAND LIMITED",
        code="G13",
        priority="normal",
        sector="Real Estate",
    ),
    Company(
        name="SEATRIUM LIMITED",
        code="STM",
        priority="normal",
        sector="Mining",
    ),
]

WATCHLIST_CODES = {
    company.code
    for company in WATCHLIST
    if company.enabled
}
