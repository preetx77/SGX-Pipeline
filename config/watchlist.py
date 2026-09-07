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
    Company(
        name="UOB S$750M3.58%PERPCAPSEC",
        code="1N1B",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SEATRIUM LTD",
        code="5E2",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MULTIPLE",
        code="7J1B",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MULTIPLE",
        code="96HB",
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
        name="SINGAPORE AIRLINES LTD",
        code="C6L",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="CITY DEVELOPMENTS LTD NCCPS",
        code="C70",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="JIUTIAN CHEMICAL GROUP LIMITED",
        code="C8R",
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
        name="MULTIPLE",
        code="FJJB",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="MULTIPLE",
        code="FJYB",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="SIA CNY1.5B2.38%N310630",
        code="GURB",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="IX BIOPHARMA LTD. W260718",
        code="HQXW",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="UOB US$35M Z460625",
        code="HYXB",
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
        name="MULTIPLE",
        code="VB9B",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="OLAM S$250M5.375% PERPSEC",
        code="VT0B",
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
        name="UOB GBP1B F300225",
        code="XXFB",
        priority="normal",
        sector="Unknown",
    ),
    Company(
        name="UOB US$150M F280724",
        code="XY4B",
        priority="normal",
        sector="Unknown",
    ),

    # Stage 3 expansion: 24 + 1 = 25 new companies (50 total)
    Company(
        name="NETLINK NBN TRUST",
        code="CJLU",
        priority="normal",
        sector="Unknown",
    ),
]
