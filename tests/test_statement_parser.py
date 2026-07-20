import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.document_repository import DocumentRepository

from parsers.statement_parser import StatementParser
from parsers.section_extractor import SectionExtractor


repo = DocumentRepository()

# Get actual financial statements, not press releases
financial_statements = repo.get_financial_statements()

if not financial_statements:
    print("No financial statement documents found")
    repo.close()
    exit(1)

doc = financial_statements[0]

section = SectionExtractor()

income_statement = section.income_statement(doc.text)

print("=" * 80)
print(doc.filename)
print("=" * 80)

parser = StatementParser()

statement = parser.parse(income_statement)

if statement:
    for key, values in statement.items():

        print("\n" + "=" * 60)
        print(key)

        for value in values:

            print("   ", value)
else:
    print("No financial data found")

repo.close()
