"""
Inspect Financial Statement Layout

This script helps us understand how SGX financial
statements are structured before writing any extractor.
"""

import sys
from pathlib import Path

# Add parent directory to path so imports work from any location
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.document_repository import DocumentRepository


def separator(title):

    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


repo = DocumentRepository()

documents = repo.get_documents_by_type("Financial Results")

print(f"\nFinancial Result Documents : {len(documents)}")

for index, document in enumerate(documents, start=1):

    separator(f"{index}. {document.filename}")

    text = document.text

    # ----------------------------------------------------
    # Find where income statement starts
    # ----------------------------------------------------

    keywords = [

        "CONDENSED INTERIM CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME",

        "STATEMENT OF COMPREHENSIVE INCOME",

        "Statement of Comprehensive Income",

        "Comprehensive Income"

    ]

    start = -1

    for keyword in keywords:

        start = text.find(keyword)

        if start != -1:
            break

    if start == -1:

        print("Income Statement NOT FOUND")
        continue

    snippet = text[start:start + 3500]

    print(snippet)

    input("\nPress ENTER for next document...")