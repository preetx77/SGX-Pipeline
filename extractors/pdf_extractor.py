# PDF EXTRACTION ENGINE : coverts downlaoded PDF into DOCUMENT OBJECT 

import fitz
from models.document import Document

class PDFExtractor:
    def extract(self, attachment, announcement) -> Document:

        pdf = fitz.open(
            attachment.local_path
        )

        pages = []
        
        for page in pdf:
            pages.append(
                page.get_text()
            )

        pdf.close()
        text = "\n".join(pages)
        word_count = len(text.split())

        return Document(
            attachment_id=attachment.attachment_id,
            announcement_id=announcement.announcement_id,
            announcement_title=announcement.title,
            announcement_category=announcement.category,
            company_name=announcement.company_name,
            stock_code=announcement.stock_code,
            filename=attachment.filename,
            local_path=attachment.local_path,
            text=text,
            page_count=len(pages),
            word_count=word_count,
            extracted=True
        )