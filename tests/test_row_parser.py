import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.document_repository import DocumentRepository

from parsers.section_extractor import SectionExtractor
from parsers.statement_parser import StatementParser
from parsers.financial_row_parser import FinancialRowParser

repo = DocumentRepository()

# Get actual financial statements, not press releases
financial_statements = repo.get_financial_statements()

if not financial_statements:
    print("No financial statement documents found")
    repo.close()
    exit(1)

doc = financial_statements[0]

section = SectionExtractor()

statement = StatementParser().parse(
    section.income_statement(doc.text)
)

parser = FinancialRowParser()

print("=" * 80)
print(f"Document: {doc.filename}")
print("=" * 80)

if statement:
    for row, values in statement.items():

        parsed = parser.parse(values)

        print(f"{row:30}")

        print(f"   Current : {parsed['current']}")

        print(f"   Previous: {parsed['previous']}")

        print(f"   Growth  : {parsed['growth']}")

        print()
else:
    print("No financial data found")

repo.close()
