import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

class AnnouncementRouter:

    @classmethod
    def is_insider(cls, announcement) -> bool:
        """
        Returns True if the announcement is related to insider dealings.
        """

        category = getattr(
            announcement,
            "category",
            ""
        ) or ""

        title = getattr(
            announcement,
            "title",
            ""
        ) or ""

        category = category.lower()
        title = title.lower()

        insider_keywords = [
            "disclosure of interest",
            "change in interest",
            "director's interest",
            "substantial shareholder",
        ]

        text = f"{category} {title}"

        return any(
            keyword in text
            for keyword in insider_keywords
        )