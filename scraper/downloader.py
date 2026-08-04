import requests
import logging
from pathlib import Path


class PDFDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.base_download_path = Path("data/raw")

    def download(self, attachment, stock_code: str, submission_date: str) -> str:
        """
        Download a PDF attachment and save it locally.
        
        Returns:
            str: The local path where the file was saved.
        """
        try:
            # Create directory structure: data/raw/{stock_code}/{year}/
            year = submission_date.split("-")[0] if "-" in submission_date else "unknown"
            download_dir = self.base_download_path / stock_code / year
            download_dir.mkdir(parents=True, exist_ok=True)

            # Download the file
            response = self.session.get(attachment.download_url, timeout=30)
            response.raise_for_status()

            # Save the file
            file_path = download_dir / attachment.filename
            with open(file_path, "wb") as f:
                f.write(response.content)

            logging.info(f"Downloaded {attachment.filename} to {file_path}")
            return str(file_path)

        except Exception as e:
            logging.error(f"Failed to download {attachment.filename}: {e}")
            raise
