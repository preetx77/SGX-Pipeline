"""
Builds human-readable notification messages.

Every notifier (Console, Telegram, Email, Slack)
uses this builder so formatting stays consistent.
"""


class MessageBuilder:

    def build(self, signal):

        message = f"""
 SGX INSIDER SIGNAL

━━━━━━━━━━━━━━━━━━━━━━

Company
{signal.company_name} ({signal.stock_code})

Director
{signal.director_name}

Transaction
{signal.transaction_type.replace("_", " ").title()}

Decision
{signal.decision}

Confidence
{signal.confidence:.1f}%

Reason
{signal.reason}

━━━━━━━━━━━━━━━━━━━━━━
"""

        return message.strip()
