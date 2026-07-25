from datetime import datetime


class AnnouncementBuilder:

    @staticmethod
    def format_date(date):

        try:
            return datetime.strptime(
                date,
                "%Y%m%d"
            ).strftime("%d %b %Y")

        except Exception:
            return date

    @staticmethod
    def build(company, announcement):

        date = AnnouncementBuilder.format_date(
            announcement.date
        )

        attachment = (
            "📎 Attachment Available"
            if announcement.attachments
            else "📄 No Attachment"
        )

        return f"""
📈 SGX Announcement

━━━━━━━━━━━━━━━━━━━━━━

Company
{company.name} ({company.code})

Sector
{company.sector}

Priority
{company.priority.upper()}

Category
{announcement.category}

Title
{announcement.title}

Date
{date}

{attachment}

━━━━━━━━━━━━━━━━━━━━━━

{announcement.url}
""".strip()