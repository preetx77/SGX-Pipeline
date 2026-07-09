#class traanslator bw my code and SGX , project shld never onow how SGX works internally

import sys
from pathlib import Path

# Fix path issues - remove conflicting paths
project_root = str(Path(__file__).parent.parent)
sys.path = [p for p in sys.path if 'calchas' not in p]
sys.path.insert(0, project_root)

import requests 

from utils.config import(
    BASE_URL,
    DEFAULT_PERIOD_START,
    DEFAULT_PERIOD_END,
    DEFAULT_PAGE_SIZE,
    HEADERS
)

class SGXClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_announcement(
        self, 
        company_name,
        page_start =0,
        page_size=DEFAULT_PAGE_SIZE,
        period_start =DEFAULT_PERIOD_START,
        period_end = DEFAULT_PERIOD_END,
    ):

        params = {
            "periodstart" : period_start,
            "periodend" : period_end,
            "value" : company_name,
            "exactsearch" : "true",
            "pagestart" : page_start,
            "pagesize" : page_size,
        }   
        
        response = self.session.get(
            BASE_URL,
            params = params,
            timeout = 30
        )
        print(response.status_code)
        print(response.text)

        return response
        

#helper 
    def get_announcments(self, company_name):
        response = self.fetch_announcement(company_name)
        return response["data"]

#helper 
    def print_summary(self, company_name):

        announcements = self.get_announcments(company_name)

        print(f"\nCompany :  {company_name}")
        print(f"Found : {len(announcements)} announcements\n" )

        for item in announcements[:5]:

            print(item["submission_date"])
            print(item["title"])
            print(item["category_name"])
            print("-" * 50)


