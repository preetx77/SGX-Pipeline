import sys
from pathlib import Path

# Add parent directory to path so imports work from any location
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.document_repository import DocumentRepository

repo = DocumentRepository()

documents = repo.get_documents_by_type(
    "Financial Results"
)

print(f"Financial Result PDFs : {len(documents)}")

for doc in documents:

    print("=" * 80)

    print(doc.filename)

    print()

    print(doc.text[:2500])

    input("\nPress Enter...")