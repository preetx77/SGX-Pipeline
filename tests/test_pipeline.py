import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.announcement_repository import AnnouncementRepository

from pipeline.sgx_pipeline import SGXPipeline


repo = AnnouncementRepository()

pipeline = SGXPipeline()


announcements = repo.latest(50)

for announcement in announcements:

    if "interest" not in announcement.title.lower():
        continue

    pipeline.process(announcement)

    break