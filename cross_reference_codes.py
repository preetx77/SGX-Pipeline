"""
Cross-reference company names against the announcement API to get codes.
Test with a sample of known companies from our watchlist.
"""
from scraper.client import SGXClient
import json

client = SGXClient()

# Known test companies with expected codes
test_companies = [
    ("OILTEK INTERNATIONAL LIMITED", "HQU"),
    ("HYPHENS PHARMA INTERNATIONAL LIMITED", "1J5"),
    ("LUM CHANG HOLDINGS LIMITED", "L19"),
    ("JUSTCO HOLDINGS LIMITED", "41A"),
]

print("Testing announcement API to retrieve codes for known companies:\n")

for company_name, expected_code in test_companies:
    print(f"Searching: {company_name}")
    try:
        # Call the announcement API with the company name
        announcements = client.get_company_announcement(
            company_name=company_name,
            page_start=0,
            page_size=1  # Get just 1 to test
        )
        
        if announcements:
            announcement = announcements[0]
            retrieved_code = announcement.stock_code
            print(f"  Result: {retrieved_code}")
            if retrieved_code == expected_code:
                print(f"  ✓ Matches expected code")
            else:
                print(f"  ⚠ Different from expected ({expected_code})")
        else:
            print(f"  ✗ No announcements found")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    print()

# Now try reverse: get company names from companylist and try to find their codes
print("\n" + "="*80)
print("Reverse mapping: Getting codes for companylist names\n")

company_list = client.get_company_list()
sample_names = company_list['data'][:20]  # First 20 names

print(f"Testing first 20 names from companylist:\n")
mapped = []

for name in sample_names:
    try:
        announcements = client.get_company_announcement(
            company_name=name,
            page_start=0,
            page_size=1
        )
        
        if announcements:
            code = announcements[0].stock_code
            mapped.append((name, code))
            print(f"✓ {name} -> {code}")
        else:
            print(f"✗ {name} -> (no announcements)")
    except Exception as e:
        print(f"✗ {name} -> Error: {type(e).__name__}")

print(f"\nSuccessfully mapped: {len(mapped)}/{len(sample_names)}")
