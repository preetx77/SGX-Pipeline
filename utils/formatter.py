from datetime import datetime

from core.classifier import Classification
from core.priority import Priority


class AnnouncementFormatter:
    """
    Formats announcements into clean Telegram messages.
    """

    @staticmethod
    def _format_date(date_str: str) -> str:
        """
        Converts:
            20260722
        into:
            22 Jul 2026
        """

        if not date_str:
            return "Unknown"

        try:
            return datetime.strptime(
                date_str,
                "%Y%m%d"
            ).strftime("%d %b %Y")

        except Exception:
            return date_str

    @staticmethod
    def _clean_title(title: str) -> str:
        """
        Removes noisy SGX prefixes.
        """

        if not title:
            return "No Title"

        prefixes = [
            "Disclosure of Interest/ Changes in Interest of Director/ Chief Executive Officer::",
            "Disclosure of Interest/ Changes in Interest of Substantial Shareholder(s)/ Unitholder(s)::",
            "Financial Statements and Related Announcement::",
            "General Announcement::",
            "Asset Acquisitions and Disposals::",
            "Request for Trading Halt::",
            "Share Buy Back - Daily Share Buy-Back Notice::",
            "Equity Listing - Ordinary Shares::",
            "Change - Announcement of Appointment::",
            "Employee Stock Option/ Share Scheme::",
            "REPL::Annual General Meeting::",
        ]

        cleaned = title

        for prefix in prefixes:
            cleaned = cleaned.replace(prefix, "")

        return cleaned.strip()

    @staticmethod
    def _attachment_status(announcement) -> str:

        attachment = getattr(
            announcement,
            "attachment_url",
            None
        )

        if attachment:
            return "📎 Available"

        return "❌ None"

    @staticmethod
    def telegram(
        announcement,
        company,
        classification: Classification,
        priority: Priority,
    ) -> str:

        company_name = getattr(
            company,
            "name",
            "Unknown Company"
        )

        company_code = getattr(
            company,
            "code",
            "N/A"
        )

        sector = getattr(
            company,
            "sector",
            "Unknown"
        )

        message = f"""
📈 <b>{company_name}</b>

🏷 <b>Ticker:</b> {company_code}

🏭 <b>Sector:</b> {sector}

━━━━━━━━━━━━━━━━━━━━

📢 <b>Event</b>

{classification.event_type.value}

🔥 <b>Priority</b>

{priority.label} ({priority.stars})

━━━━━━━━━━━━━━━━━━━━

📰 <b>Headline</b>

{AnnouncementFormatter._clean_title(announcement.title)}

━━━━━━━━━━━━━━━━━━━━

📅 <b>Date</b>

{AnnouncementFormatter._format_date(
    announcement.date
)}

📎 <b>Attachment</b>

{AnnouncementFormatter._attachment_status(
    announcement
)}

━━━━━━━━━━━━━━━━━━━━

🔗 <b>Announcement ID</b>

{announcement.id}
"""

        return message.strip()