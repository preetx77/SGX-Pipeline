"""
Live tests for SGX API access.
Run with: pytest -m live

These tests verify that:
1. Each company can be queried for announcements
2. Announcements are returned (not zero for known issuers)
3. The measurement data is valid for all companies
"""

import pytest
from tests.conftest import companies as load_companies


@pytest.mark.live
class TestSGXClientAccess:
    """Live tests for SGX API access"""
    
    @pytest.fixture
    def companies(self):
        """Load companies fixture"""
        with open("tests/fixtures/companies.json") as f:
            import json
            return json.load(f)
    
    @pytest.mark.parametrize("company", 
        [c for c in __import__('json').load(open("tests/fixtures/companies.json"))],
        ids=lambda c: c["code"]
    )
    def test_returns_announcements(self, company, client, time_range):
        """Each company must return announcements (not zero)"""
        announcements = list(client.iter_company_announcements(
            company['name'],
            period_start=time_range['period_start'],
            period_end=time_range['period_end'],
            page_size=100
        ))
        
        assert len(announcements) > 0, \
            f"{company['code']} ({company['name']}) returned zero announcements - measurement failed"
    
    @pytest.mark.parametrize("company",
        [c for c in __import__('json').load(open("tests/fixtures/companies.json"))],
        ids=lambda c: c["code"]
    )
    def test_has_director_filings(self, company, client, time_range):
        """Each company must have at least one director filing in measured data"""
        announcements = list(client.iter_company_announcements(
            company['name'],
            period_start=time_range['period_start'],
            period_end=time_range['period_end'],
            page_size=100
        ))
        
        director_count = sum(1 for a in announcements 
                            if 'FORM 1' in (a.get('title', '') or '').upper())
        
        assert director_count >= company['min_director_filings'], \
            f"{company['code']}: found {director_count} director filings, expected ≥{company['min_director_filings']}"

