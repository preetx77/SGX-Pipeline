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

    # Stage 3 expansion: 50 new companies
    Company(
        name="ASIAINVEST HOLDINGS CORP",
        code="AIHC",
        priority="normal",
        sector="Finance",
    ),
    Company(
        name="ASIACORP LIMITED",
        code="ASIACORP",
        priority="normal",
        sector="Conglomerate",
    ),
    Company(
        name="ASIAJET AIRWAYS",
        code="AJA",
        priority="normal",
        sector="Aviation",
    ),
    Company(
        name="ASIAINSURANCE BERHAD",
        code="ASINS",
        priority="normal",
        sector="Insurance",
    ),
    Company(
        name="ASIAINFO TECHNOLOGIES LIMITED",
        code="ASII",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="ASIAHUB TECHNOLOGY CORP",
        code="AHTC",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="ASIAHEALTH CORPORATION",
        code="AHC",
        priority="normal",
        sector="Healthcare",
    ),
    Company(
        name="ASIAGOLD MINING CORP",
        code="AGMC",
        priority="normal",
        sector="Mining",
    ),
    Company(
        name="ASIAFLOW LOGISTICS LIMITED",
        code="AFL",
        priority="normal",
        sector="Logistics",
    ),
    Company(
        name="ASIACOM TELECOM CORP",
        code="ATCOM",
        priority="normal",
        sector="Telecom",
    ),
    Company(
        name="ASIACHEM CORPORATION",
        code="ACHEM",
        priority="normal",
        sector="Chemical",
    ),
    Company(
        name="ASIAZONE INTERACTIVE CORP",
        code="AZIC",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="ASIAWORLD CORPORATION",
        code="ASIAW",
        priority="normal",
        sector="Conglomerate",
    ),
    Company(
        name="ASIAPACIFIC TECH HOLDINGS",
        code="APTH",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="ASIAPACIFIC MANUFACTURING CORP",
        code="APMC",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="ASIAPACIFIC ENERGY CORP",
        code="APEC",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="ASIATRANSP LOGISTICS CORP",
        code="ALC",
        priority="normal",
        sector="Logistics",
    ),
    Company(
        name="ASIAVALUE CORP",
        code="AVC",
        priority="normal",
        sector="Finance",
    ),
    Company(
        name="ASIATRADE HOLDINGS CORP",
        code="AHC",
        priority="normal",
        sector="Trade",
    ),
    Company(
        name="ASIATECH CORPORATION",
        code="ASIATECH",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="ASIANFOOD CORP LIMITED",
        code="AFCL",
        priority="normal",
        sector="Food & Beverage",
    ),
    Company(
        name="ASIAN DEVELOPMENT BANK",
        code="ADB",
        priority="normal",
        sector="Finance",
    ),
    Company(
        name="ASIAN DEFENSE CORPORATION",
        code="ADC",
        priority="normal",
        sector="Defense",
    ),
    Company(
        name="ASIAN ELECTRONICS AND TRADING CORP",
        code="AETC",
        priority="normal",
        sector="Electronics",
    ),
    Company(
        name="ASIAWEEK MEDIA CORPORATION",
        code="AWMC",
        priority="normal",
        sector="Media",
    ),
    Company(
        name="ASIA BEVERAGE LIMITED",
        code="ABL",
        priority="normal",
        sector="Food & Beverage",
    ),
    Company(
        name="ASIA INVESTMENT MANAGEMENT LIMITED",
        code="AIML",
        priority="normal",
        sector="Finance",
    ),
    Company(
        name="ASIA ENERGY CORP LIMITED",
        code="AEC",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="ASIA TECHNOLOGIES CORPORATION",
        code="ATC",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="ASIA RARE EARTH LLC",
        code="ARE",
        priority="normal",
        sector="Mining",
    ),
    Company(
        name="ASIA MEDIA GROUP CORP",
        code="AMGC",
        priority="normal",
        sector="Media",
    ),
    Company(
        name="ASIA WATER TECHNOLOGY LIMITED",
        code="AWTL",
        priority="normal",
        sector="Utilities",
    ),
    Company(
        name="ASIA PACIFIC INVESTMENT LIMITED",
        code="APIL",
        priority="normal",
        sector="Finance",
    ),
    Company(
        name="ASIA PACIFIC WIRE AND CABLE CORPORATION LIMITED",
        code="APWC",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="ASIA LOGISTICS PROPERTIES LIMITED",
        code="ALP",
        priority="normal",
        sector="Logistics",
    ),
    Company(
        name="CHINA PHARMA",
        code="CP",
        priority="normal",
        sector="Healthcare",
    ),
    Company(
        name="CHINA RECYCLING",
        code="CR",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="CHINA TECH FIBER CORPORATION",
        code="CTFC",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="CHINA XD PLASTICS",
        code="CXDP",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="CHINA YADA HOLDING GROUP CORP",
        code="CYHG",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="CHINA SUN ENERGY SOLUTION LIMITED",
        code="CSES",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="CHINA COMMERCIAL CREDIT INC",
        code="CCCI",
        priority="normal",
        sector="Finance",
    ),
    Company(
        name="CHINA NATURALS INC",
        code="CNAT",
        priority="normal",
        sector="Agriculture",
    ),
    Company(
        name="CHINA INTEGRATED ENERGY LIMITED",
        code="CIEL",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="CHINA XD PLASTICS COMPANY LIMITED",
        code="CXDC",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="CHINA SOS LIMITED",
        code="CHL",
        priority="normal",
        sector="Manufacturing",
    ),
    Company(
        name="CHINA RECYCLING ENERGY CORP",
        code="CREC",
        priority="normal",
        sector="Energy",
    ),
    Company(
        name="CHINA PHARMA HOLDINGS INC",
        code="CPHI",
        priority="normal",
        sector="Healthcare",
    ),
    Company(
        name="HSTECH INVESTMENT LIMITED",
        code="HSTECH",
        priority="normal",
        sector="Technology",
    ),
    Company(
        name="GAMIN LIMITED",
        code="G08",
        priority="normal",
        sector="Technology",
    ),
]

WATCHLIST_CODES = {
    company.code
    for company in WATCHLIST
    if company.enabled
}
