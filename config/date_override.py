"""
Date override for environments with incorrect system time.

The SGX environment runs on Nov 2026 clock, but the measurement data
was collected in Oct 2026. The SGX API validates that:
  - period_end <= system_now
  - period_start < period_end

Solution: Use the system's current time for API queries (Nov 2026).
The API will accept it even though historical data only goes to Oct 2026.
"""

from datetime import datetime, timedelta

def get_api_query_dates(lookback_days=1825):
    """
    Get date range for SGX API queries using SYSTEM dates.
    
    The system date is in the future (Nov 2026), but SGX API requires
    dates to be <= system_now. We use system time for valid API requests.
    
    Args:
        lookback_days: How many days back to query (default: 5 years = 1825 days)
    
    Returns:
        dict with timestamps and datetime objects for API queries
    """
    # Use actual system time (Nov 2026 on this machine)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=lookback_days)
    
    return {
        'end': end_date,
        'start': start_date,
        'period_end': int(end_date.timestamp()),
        'period_start': int(start_date.timestamp()),
        'end_date': end_date,
        'start_date': start_date,
    }

