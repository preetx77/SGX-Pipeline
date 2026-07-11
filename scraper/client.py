"""
SGX API Client

Responsible only for communicating with SGX APIs.
"""

import requests

from models.announcement import Announcement
from scraper.auth import AuthenticationManager
from config.settings import (
    ANNOUNCEMENT_API,
    USER_AGENT
)


class SGXClient:

    def __init__(self):

        self.auth = AuthenticationManager()

        self.session = requests.Session()

        self.session.headers.update({

            "Accept": "application/json",

            "User-Agent": USER_AGENT,

            "Origin": "https://www.sgx.com",

            "Referer": "https://www.sgx.com/",

        })

        self.base_url = ANNOUNCEMENT_API

        self._authenticate()

# instead of headers, inside every API , we auhtneticate once , then every req automatically carries authoirzation 

    def _authenticate(self):

        token = self.auth.get_token()

        self.session.headers.update({

            "authorizationToken": token

        })

    def refresh_authentication(self):

        token = self.auth.refresh_token()

        self.session.headers.update({

            "authorizationToken": token

        })

    def _get(self, endpoint, params=None):
        """Generic GET request handler"""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(
            url,
            params=params,
            timeout=30
        )
        print(f"Status Code : {response.status_code}")
        response.raise_for_status()
        return response.json()

    def get_company_list(self):
        # Fetch list of all companies
        return self._get("companylist")

    def get_company_announcement(
        self,
        company_name,
        page_start=0,
        page_size=100,
        period_start=None,
        period_end=None
    ):

        params = {
            "periodstart" : period_start,
            "periodend" : period_end,
            "value" : company_name,
            "exactsearch": "true",
            "pagestart" : page_start,
            "pagesize" : page_size
        }

        response = self._get(
            "company",
            params=params
        )

        announcements = []

        for item in response.get("data", []):
            announcements.append(
                self._json_to_announcement(item)
            )

        return announcements

# Function would be the heart of client : every sgx json will pass through here exactly once
# Convert raw SGX API JSON into an Announcement object.
    
    def _json_to_announcement(self, item: dict) -> Announcement:

        issuer = item.get("issuers", [{}])[0]  # Get first issuer from list
        return Announcement(
            announcement_id=item.get("id"),
            ref_id=item.get("ref_id"),
            company_name=item.get("security_name"),
            stock_code=issuer.get("stock_code"),
            isin_code=issuer.get("isin_code"),
            title=item.get("title"),
            category=item.get("category_name"),
            category_code=item.get("cat"),
            subcategory_code=item.get("sub"),
            announcement_url=item.get("url"),
            submission_date=item.get("submission_date"),
            submission_timestamp=item.get("submission_date_time"),
            submitted_by=item.get("submitted_by"),
        )