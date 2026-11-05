import json
import pytest
from datetime import datetime, timedelta
from scraper.client import SGXClient


@pytest.fixture(scope="session")
def companies():
    """Load test company data from fixtures"""
    with open("tests/fixtures/companies.json") as f:
        return json.load(f)


@pytest.fixture
def client():
    """Provide SGX client for live tests"""
    return SGXClient(throttle_delay=1.0)


@pytest.fixture
def time_range():
    """Provide a standard time range for tests (last 2 years)"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=730)
    return {
        'period_start': int(start_date.timestamp()),
        'period_end': int(end_date.timestamp()),
        'start_date': start_date,
        'end_date': end_date
    }

