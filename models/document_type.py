
# Document Types


from enum import Enum


class DocumentType(Enum):

    UNKNOWN = "Unknown"

    FINANCIAL_RESULTS = "Financial Results"

    ANNUAL_REPORT = "Annual Report"

    INTERIM_REPORT = "Interim Report"

    GENERAL_ANNOUNCEMENT = "General Announcement"

    DIRECTOR_DEALINGS = "Director Dealings"

    DIVIDEND = "Dividend"

    AGM = "AGM"

    EGM = "EGM"

    PRESENTATION = "Presentation"

    CIRCULAR = "Circular"

    TRADING_UPDATE = "Trading Update"

    CONTRACT = "Contract"

    ACQUISITION = "Acquisition"

    DISPOSAL = "Disposal"

    SHARE_BUYBACK = "Share Buyback"

    OTHER = "Other"





    """
Why Enum? 
Suppose later you accidentally write
"financial results"
"FinancialResults
"Financial Result"
"Results"

Now every downstream module breaks.Instead, everyone uses

DocumentType.FINANCIAL_RESULTS

One source of truth.
    """