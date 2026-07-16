
# Extractor Factory : Chooses the correct extractor based on the document type.


from models.document_type import DocumentType
from extractors.financial_results_extractor import (
    FinancialResultsExtractor,
)

class ExtractorFactory:

    def get_extractor(self, document_type):

        if document_type == DocumentType.FINANCIAL_RESULTS:
            return FinancialResultsExtractor()

        return None