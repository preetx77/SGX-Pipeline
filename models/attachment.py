

from dataclasses import dataclass
import hashlib


@dataclass(slots=True)
class Attachment:

    attachment_id: str

    announcement_id: str

    filename: str

    download_url: str

    file_size: str | None = None

    local_path: str | None = None

    downloaded: bool = False

    @staticmethod
    def generate_id(
        announcement_id: str,
        download_url: str
    ) -> str:

        text = f"{announcement_id}:{download_url}"

        return hashlib.sha256(
            text.encode()
        ).hexdigest()

    def __str__(self):

        return (
            f"{self.filename} "
            f"({'Downloaded' if self.downloaded else 'Pending'})"
        )

""" Why SHA256?
Suppose tomorrow SGX changes filenames.
Example : AnnualReport.pdf

becomes

Annual_Report_2025.pdf

so  : The URL remains the same. Our ID remains the same. No duplicate.
"""
