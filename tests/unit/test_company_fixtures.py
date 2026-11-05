"""
Offline unit tests for company fixtures.
Verifies that test data and production watchlist stay in sync.
"""

import json
import pytest
from config.watchlist import WATCHLIST


@pytest.fixture
def companies():
    """Load company fixtures"""
    with open("tests/fixtures/companies.json") as f:
        return json.load(f)


@pytest.fixture
def watchlist_codes():
    """Load codes from production watchlist"""
    return {c.code for c in WATCHLIST}


class TestCompanyFixtures:
    """Test company fixture data integrity"""
    
    def test_companies_json_is_valid(self, companies):
        """Companies fixture must be valid JSON with required fields"""
        assert isinstance(companies, list)
        assert len(companies) == 32
        
        for c in companies:
            assert 'code' in c, f"Missing 'code' in {c}"
            assert 'name' in c, f"Missing 'name' in {c}"
            assert 'min_director_filings' in c, f"Missing 'min_director_filings' in {c}"
    
    @pytest.mark.parametrize("company", [
        json.loads(open("tests/fixtures/companies.json").read())
    ][0])
    def test_code_is_valid_sgx_code(self, company):
        """SGX codes must be 1-4 alphanumeric characters"""
        code = company['code']
        assert 1 <= len(code) <= 4, f"Code {code} is {len(code)} chars, expected 1-4"
        assert code.isalnum(), f"Code {code} contains non-alphanumeric characters"
    
    def test_codes_are_unique(self, companies):
        """All company codes must be unique"""
        codes = [c['code'] for c in companies]
        assert len(codes) == len(set(codes)), f"Duplicate codes found: {codes}"
    
    def test_companies_match_watchlist(self, companies, watchlist_codes):
        """Company fixtures must match production watchlist codes"""
        fixture_codes = {c['code'] for c in companies}
        assert fixture_codes == watchlist_codes, \
            f"Fixture codes {fixture_codes} != watchlist codes {watchlist_codes}"
    
    def test_min_director_filings_is_positive(self, companies):
        """All companies must have at least 1 director filing"""
        for c in companies:
            assert c['min_director_filings'] >= 1, \
                f"{c['code']} has {c['min_director_filings']} director filings, expected ≥1"

