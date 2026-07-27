
# SGX API Client : Responsible only for communicating with SGX APIs

import requests
import logging

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
        url = f"{self.base_url}/{endpoint}"

        logging.debug(f"GET request to {url} with params: {params}")

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=30
            )

            logging.debug(f"Response status: {response.status_code}")

            # Handle specific error codes
            if response.status_code == 404:
                logging.error(f"Endpoint not found: {url}")
                raise requests.HTTPError(f"404 Not Found: {url}", response=response)
            elif response.status_code == 429:
                logging.warning(f"Rate limited (429) on {url}")
                raise requests.HTTPError(f"429 Too Many Requests", response=response)
            elif response.status_code >= 500:
                logging.error(f"Server error ({response.status_code}) on {url}")
                raise requests.HTTPError(f"Server error {response.status_code}", response=response)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logging.error(f"Timeout fetching {url}")
            raise
        except requests.exceptions.ConnectionError:
            logging.error(f"Connection error fetching {url}")
            raise
        except ValueError as e:
            logging.error(f"Failed to parse JSON response from {url}: {e}")
            raise
        except requests.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            raise

        
    def get_company_list(self):
        # Fetch list of all companies
        return self._get("companylist")


# ----------------------------------------------------------------------

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
            "pagestart" : page_start,
            "pagesize" : page_size
        }

        response = self._get(
            "company",
            params=params
        )

        data = response.get("data") or []

        announcements = []

        for item in data:
            try:
                announcements.append(
                    self._json_to_announcement(item)
                )
            except Exception:
                logging.exception(
                    "Failed parsing announcement."
                )

        return announcements
    # ----------------------------------------------------------------------------------------

    def get_company_announcement_page(
        self,
        company_name,
        page_start=0,
        page_size=100,
        period_start=None,
        period_end=None
    ):
        params = {
             "periodstart": period_start,
            "periodend": period_end,
            "value": company_name,
            "pagestart": page_start,
            "pagesize": page_size
        }

        response = self._get("company", params = params)

        if response is None:
            return {"meta" : {}, "announcements" : []}

        raw_data = response.get("data") or []

        announcements = [
            self._json_to_announcement(item)
            for items in raw_data
        ]

        return {
            "meta": response.get("meta", {}),
            "announcement" : announcements
        }
    

    # --------------------------------------------------------------------------------------

    def iter_company_announcements(
        self,
        company_name,
        period_start,
        period_end,
        page_size=100
    ):

        page_start = 0
        
        while True:
            result = self.get_company_announcement_page(
                company_name = company_name,
                page_start = page_start,
                page_size = page_size,
                period_start = period_start,
                period_end = period_end
            )
            announcements = result["announcements"]

            if not announcements:
                break
            for announcement in announcements:
                yield announcement

            if len(announcements) < page_size:
                break
        
            page_start += page_size


    # ------------------------------------------------------------------------------------

# Function would be the heart of client : every sgx json will pass through here exactly once
# Convert raw SGX API JSON into an Announcement object.
    
    def _json_to_announcement(self, item: dict) -> Announcement:

        issuers = item.get("issuers") or []
        issuer = issuers[0] if issuers else {}  # Get first issuer from list
        
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