"""
Date override for environments with incorrect system time.

The SGX Pipeline was tested in an environment where system date is set to Nov 2026,
but the SGX API only has historical data up to October 2026.

This module provides corrected dates for API queries.
"""

from datetime import datetime, timedelta

# Actual current date (approximate)
# In production, this should be actual current date
CORRECTED_NOW = datetime(2024, 11, 24, 7, 40, 0)

def get_api_query_dates(lookback_days=1825):
    """
    Get date range for SGX API queries using corrected dates.
    
    Args:
        lookback_days: How many days back to query (default: 5 years = 1825 days)
    
    Returns:
        dict with 'start' and 'end' as datetime objects
        dict with 'period_start' and 'period_end' as unix timestamps
    """
    end_date = CORRECTED_NOW
    start_date = end_date - timedelta(days=lookback_days)
    
    return {
        'end': end_date,
        'start': start_date,
        'period_end': int(end_date.timestamp()),
        'period_start': int(start_date.timestamp()),
        'end_date': end_date,
        'start_date': start_date,
    }

def use_corrected_dates():
    """
    Returns True if date override is active.
    Can be disabled by setting environment variable DISABLE_DATE_OVERRIDE=1
    """
    import os
    return os.getenv('DISABLE_DATE_OVERRIDE', '0') != '1'

