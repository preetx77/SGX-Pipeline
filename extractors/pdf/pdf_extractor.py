# PDF EXTRACTION ENGINE : coverts downlaoded PDF into DOCUMENT OBJECT 

import fitz
import logging
from models.document import Document

class PDFExtractor:
    def extract(self, attachment, announcement) -> Document:
        """
        Extract text from PDF with robust error handling.
        Returns Document object even if extraction fails partially.
        """
        try:
            pdf = fitz.open(attachment.local_path)
        except Exception as e:
            logging.error(f"Failed to open PDF {attachment.filename}: {e}")
            # Return document with empty text if PDF is corrupted
            return Document(
                attachment_id=attachment.attachment_id,
                announcement_id=announcement.announcement_id,
                announcement_title=announcement.title,
                announcement_category=announcement.category,
                company_name=announcement.company_name,
                stock_code=announcement.stock_code,
                filename=attachment.filename,
                local_path=attachment.local_path,
                text="",
                page_count=0,
                word_count=0,
                extracted=False,
                metadata={"extraction_error": str(e)}
            )

        pages = []
        page_errors = 0
        
        try:
            for page_num, page in enumerate(pdf):
                try:
                    page_text = page.get_text()
                    pages.append(page_text)
                except Exception as e:
                    logging.warning(
                        f"Failed to extract page {page_num} from {attachment.filename}: {e}"
                    )
                    page_errors += 1
                    pages.append("")  # Add empty page
        except Exception as e:
            logging.error(f"PDF iteration failed for {attachment.filename}: {e}")
        finally:
            try:
                pdf.close()
            except Exception as e:
                logging.warning(f"Failed to close PDF {attachment.filename}: {e}")

        text = "\n".join(pages)
        word_count = len(text.split()) if text else 0

        # Log if we had extraction issues
        if page_errors > 0:
            logging.warning(
                f"Extracted {len(pages) - page_errors}/{len(pages)} pages from {attachment.filename}"
            )

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
            extracted=len(pages) > 0 and page_errors == 0,
            metadata={"page_errors": page_errors}
        )