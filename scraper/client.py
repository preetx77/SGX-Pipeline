"""
SGX API Client

Responsible only for communicating with SGX APIs.
"""

import requests

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
        """Fetch list of all companies"""
        return self._get("companylist")