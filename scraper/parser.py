# announcmenet HTML parser 

import requests
from bs4 import BeautifulSoup
from models.attachment import Attachment

class AnnouncementParser:

    def __init__(self):
        self.session = requests.Session()

    def _fetch_html(
        self,
        url: str
    ) -> str:
        response = self.session.get(url, timeout=30)

        response.raise_for_status()
        return response.text


# -------- parser function ------------
    def parse(self, announcement):
        
        html = self._fetch_html(announcement.announcement_url)
        soup = BeautifulSoup(html, "html.parser")
        
        attachment_links = soup.select("a.announcement-attachment")
        attachments = []

        for link in attachment_links:

            filename = link.get_text(strip=True)
            href = link.get("href")

            if href.startswith("/"):
                href = "https://links.sgx.com" + href

            attachment = Attachment(
                attachment_id = Attachment.generate_id(
                    announcement.announcement_id,
                    href
                ),

                announcement_id = announcement.announcement_id,
                filename = filename,
                download_url = href
            )
            
            attachments.append(attachment)

        return attachments


""" Why BeautifulSoup?
We already know, from your reverse engineering , that the HTML contains

<a class="announcement-attachment">

So

soup.select(
    "a.announcement-attachment"
)

directly extracts every downloadable attachment., No regex , No brittle parsing.
"""