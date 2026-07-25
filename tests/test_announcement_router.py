import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from types import SimpleNamespace

from types import SimpleNamespace

from pipeline.announcement_router import AnnouncementRouter


def test_detects_by_category():

    announcement = SimpleNamespace(
        category="Disclosure of Interest/ Changes in Interest"
    )

    assert AnnouncementRouter.is_insider(announcement)


def test_detects_by_title():

    announcement = SimpleNamespace(
        category="General Announcement",
        title="Disclosure of Interest of Director"
    )

    assert AnnouncementRouter.is_insider(announcement)


def test_rejects_financial_results():

    announcement = SimpleNamespace(
        category="Financial Statements",
        title="Half Year Results"
    )

    assert not AnnouncementRouter.is_insider(announcement)


def test_handles_missing_title():

    announcement = SimpleNamespace(
        category="Disclosure of Interest"
    )

    assert AnnouncementRouter.is_insider(announcement)


def test_handles_missing_category():

    announcement = SimpleNamespace(
        title="Disclosure of Interest"
    )

    assert AnnouncementRouter.is_insider(announcement)


def test_handles_both_missing():

    announcement = SimpleNamespace()

    assert not AnnouncementRouter.is_insider(announcement)