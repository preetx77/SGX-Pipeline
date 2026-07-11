#represents one SGX announcement : 

from dataclasses import dataclass 

@dataclass(slots=True)
class Announcement:

    announcement_id: str
    ref_id: str
    company_name: str
    stock_code: str
    isin_code: str
    title: str
    category: str
    category_code: str
    subcategory_code: str
    announcement_url: str
    submission_timestamp: int
    submission_date: str
    submitted_by: str

    def __str__(self):

        return (
            f"[{self.stock_code}] "
            f"{self.submission_date} | "
            f"{self.category} | "
            f"{self.title}"
        )

