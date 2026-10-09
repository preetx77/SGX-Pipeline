"""Inspect the actual structure of companylist response"""
import json
from scraper.client import SGXClient

client = SGXClient()
response = client.get_company_list()

print("Top-level keys:", response.keys())
print("\nMeta structure:")
print(json.dumps(response.get('meta', {}), indent=2))

print("\nFirst 10 records from 'data':")
data = response.get('data', [])
print(f"Total records: {len(data)}")
print(f"Type of first record: {type(data[0])}")

# Check if records are strings or dicts
for i, record in enumerate(data[:10]):
    if isinstance(record, dict):
        print(f"  Record {i}: {record}")
    else:
        print(f"  Record {i}: {record} (type: {type(record).__name__})")

# Check if there's any structure with codes
print("\nSearching for stock_code or code field in first 50 records:")
found_structure = False
for record in data[:50]:
    if isinstance(record, dict):
        if 'stock_code' in record or 'code' in record or 'ticker' in record:
            print(f"  Found structure: {record}")
            found_structure = True
            break

if not found_structure:
    print("  No codes found in dict records")
    if isinstance(data[0], dict):
        print(f"  Available fields: {data[0].keys()}")
