# Document Model : represnts the extracted contecnts of one pdf

from dataclasses import dataclass, field
from models.document_type import DocumentType




@dataclass(slots=True)
class Document:
    attachment_id: str

    announcement_id: str
    
    announcement_title: str

    announcement_category: str

    company_name: str

    stock_code: str

    filename: str

    local_path: str

    text: str

    page_count: int

    document_type: DocumentType = DocumentType.UNKNOWN

    extracted: bool = False

    metadata: dict = field(default_factory=dict)

    def word_count(self) -> int:

        return len(self.text.split())

    def __str__(self):

        return (
            f"[{self.stock_code}] "
            f"{self.filename} "
            f"({self.page_count} pages)"
        )