# PDF DOWNLOADER

"""
PDF Downloader
"""

from pathlib import Path
import requests


class PDFDownloader:

    def __init__(self):
        self.session = requests.Session()
        self.base_directory = Path("data/raw")

    def download(
        self,
        attachment,
        stock_code,
        submission_date
    ):
        year = submission_date[:4]
        folder = self.base_directory / stock_code / year

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = folder / attachment.filename
        response = self.session.get(

            attachment.download_url,
            timeout=60
        )

        response.raise_for_status()

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                response.content
            )

        return str(file_path)