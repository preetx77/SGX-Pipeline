"""
Weighted Document Classifier
"""

from collections import defaultdict

from models.document_type import DocumentType


class DocumentClassifier:

    def classify(self, document):

        scores = defaultdict(int)

        text = document.text.lower()

        filename = document.filename.lower()

        title = document.announcement_title.lower()

        category = document.announcement_category.lower()

        # ==========================================================
        # SGX METADATA (Highest Confidence)
        # ==========================================================

        if "general announcement" in category:
            scores[DocumentType.GENERAL_ANNOUNCEMENT] += 100

        if "financial statements" in category:
            scores[DocumentType.FINANCIAL_RESULTS] += 100

        if "cash dividend" in category:
            scores[DocumentType.DIVIDEND] += 100

        if "disclosure of interest" in category:
            scores[DocumentType.DIRECTOR_DEALINGS] += 100

        if "annual reports" in category:
            scores[DocumentType.ANNUAL_REPORT] += 100

        if "annual general meeting" in category:
            scores[DocumentType.AGM] += 100

        # ==========================================================
        # TITLE
        # ==========================================================

        if "annual report" in title:
            scores[DocumentType.ANNUAL_REPORT] += 40

        if "financial statements" in title:
            scores[DocumentType.FINANCIAL_RESULTS] += 40

        if "dividend" in title:
            scores[DocumentType.DIVIDEND] += 40

        if "general announcement" in title:
            scores[DocumentType.GENERAL_ANNOUNCEMENT] += 40

        if "annual general meeting" in title:
            scores[DocumentType.AGM] += 40

        if "director" in title:
            scores[DocumentType.DIRECTOR_DEALINGS] += 40

        # ==========================================================
        # FILENAME
        # ==========================================================

        if "annual report" in filename:
            scores[DocumentType.ANNUAL_REPORT] += 20

        if "dividend" in filename:
            scores[DocumentType.DIVIDEND] += 20

        if "agm" in filename:
            scores[DocumentType.AGM] += 20

        if "presentation" in filename:
            scores[DocumentType.PRESENTATION] += 20

        if "results" in filename:
            scores[DocumentType.FINANCIAL_RESULTS] += 20

        # ==========================================================
        # DOCUMENT TEXT (Lowest Confidence)
        # ==========================================================

        if "financial statements" in text:
            scores[DocumentType.FINANCIAL_RESULTS] += 10

        if "cash dividend" in text:
            scores[DocumentType.DIVIDEND] += 10

        if "annual report" in text:
            scores[DocumentType.ANNUAL_REPORT] += 10

        if "annual general meeting" in text:
            scores[DocumentType.AGM] += 10

        if "director's interest" in text:
            scores[DocumentType.DIRECTOR_DEALINGS] += 10

        if "disclosure of interest" in text:
            scores[DocumentType.DIRECTOR_DEALINGS] += 10

        if "changes in interest" in text:
            scores[DocumentType.DIRECTOR_DEALINGS] += 10

        if "general announcement" in text:
            scores[DocumentType.GENERAL_ANNOUNCEMENT] += 10

        # ==========================================================
        # NO MATCH
        # ==========================================================

        if len(scores) == 0:
            return DocumentType.OTHER

        return max(scores, key=scores.get)