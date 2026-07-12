# announcement service
# cordinates the SGC client and repository


from scraper.client import SGXClient
from database.repository import AnnouncementRepository

class AnnouncementService:

    def __init__(self):
        self.client = SGXClient()
        self.repository = AnnouncementRepository()

    def sync_company(
        self,
        company_name,
        period_start,
        period_end
    ):

        announcements = self.client.get_company_announcement(
            company_name,
            period_start = period_start,
            period_end = period_end
        )
        
        inserted = 0
        skipped = 0

        for announcement in announcements:
            if self.repository.insert(announcement):
                inserted+= 1
            else:
                skipped += 1
            
        return {
            "company" : company_name,
            "fetched" : len(announcements),
            "inserted" : inserted,
            "skipped" : skipped
        }

    def close(self):
        self.repository.close()


""" 
prevvioulsy main.py > client > repo

now :   main.py > service 

"""