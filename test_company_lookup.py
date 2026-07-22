from scraper.client import SGXClient

client = SGXClient()

companies = client.get_company_list()

for company in companies["data"]:
    if "OIL" in company.upper():
        print(company)