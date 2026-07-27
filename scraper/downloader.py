# PDF DOWNLOADER

"""
PDF Downloader with retry logic and comprehensive error handling.
"""

from pathlib import Path
import requests
import logging
import time

class PDFDownloader:

    def __init__(self, max_retries=3, retry_delay=2):
        self.session = requests.Session()
        self.base_directory = Path("data/raw")
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def download(
        self,
        attachment,
        stock_code,
        submission_date
    ):
        """
        Download PDF with retry logic and error handling.
        
        Raises:
            requests.RequestException: If download fails after retries
        """
        year = submission_date[:4]
        folder = self.base_directory / stock_code / year

        try:
            folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create download directory {folder}: {e}")
            raise

        file_path = folder / attachment.filename

        for attempt in range(1, self.max_retries + 1):
            try:
                logging.info(
                    f"Downloading {attachment.filename} (attempt {attempt}/{self.max_retries})"
                )
                
                response = self.session.get(
                    attachment.download_url,
                    timeout=60
                )

                # Check for HTTP errors
                if response.status_code == 404:
                    logging.error(f"Attachment not found: {attachment.download_url}")
                    raise requests.HTTPError("404 Not Found", response=response)
                elif response.status_code == 429:
                    logging.warning(f"Rate limited (429), retrying after delay...")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay * attempt)
                        continue
                    raise requests.HTTPError("429 Too Many Requests", response=response)
                elif response.status_code >= 500:
                    logging.warning(f"Server error ({response.status_code}), retrying...")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay * attempt)
                        continue
                    raise requests.HTTPError(f"Server error {response.status_code}", response=response)

                response.raise_for_status()

                # Verify content
                if not response.content:
                    logging.warning(f"Downloaded empty file for {attachment.filename}")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)
                        continue
                    raise ValueError("Downloaded file is empty")

                # Write to file
                with open(file_path, "wb") as file:
                    file.write(response.content)

                logging.info(f"Successfully downloaded {attachment.filename} ({len(response.content)} bytes)")
                return str(file_path)

            except requests.exceptions.Timeout:
                logging.warning(f"Timeout downloading {attachment.filename} (attempt {attempt}/{self.max_retries})")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)
                    continue
                raise
            except requests.exceptions.ConnectionError:
                logging.warning(f"Connection error downloading {attachment.filename} (attempt {attempt}/{self.max_retries})")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)
                    continue
                raise
            except requests.RequestException as e:
                logging.error(f"Download failed for {attachment.filename}: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)
                    continue
                raise
            except Exception as e:
                logging.error(f"Unexpected error downloading {attachment.filename}: {e}")
                raise