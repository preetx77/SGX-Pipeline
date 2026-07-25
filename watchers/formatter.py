from datetime import datetime


class AnnouncementFormatter:

    @staticmethod
    def format_date(date_str):
        """
        Converts:
        20260722 -> 22 Jul 2026
        """

        try:
            return datetime.strptime(
                date_str,
                "%Y%m%d"
            ).strftime("%d %b %Y")

        except Exception:
            return date_str

    @staticmethod
    def clean_title(title):

        if not title:
            return "No Title"

        prefixes = [
            "General Announcement::",
            "Financial Statements and Related Announcement::",
            "Disclosure of Interest/ Changes in Interest of Director/ Chief Executive Officer::",
            "Disclosure of Interest/ Changes in Interest of Substantial Shareholder(s)/ Unitholder(s)::",
            "Asset Acquisitions and Disposals::",
            "Request for Trading Halt::",
            "Equity Listing - Ordinary Shares::",
            "Employee Stock Option/ Share Scheme::",
            "Share Buy Back - Daily Share Buy-Back Notice::",
        ]

        for prefix in prefixes:
            if title.startswith(prefix):
                return title.replace(prefix, "").strip()

        return title

    @staticmethod
    def telegram(company, announcement):

        title = AnnouncementFormatter.clean_title(announcement.title)

        date = AnnouncementFormatter.format_date(announcement.date)

        pdf = ("📎 PDF Available"if announcement.attachmentselse "📄 No Attachment")

        return (
            f"📈 {company.name}\n"
            f"({company.code})\n\n"
            f"🏷 Category: {announcement.category}\n"
            f"📰 {title}\n"
            f"📅 {date}\n"
            f"🏭 Sector: {company.sector}\n"
            f"🔥 Priority: {company.priority.upper()}\n"
            f"{pdf}\n\n"
            f"🔗 {announcement.url}"
        )