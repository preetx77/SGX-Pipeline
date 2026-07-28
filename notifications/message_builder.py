"""
Builds human-readable notification messages.

Every notifier (Console, Telegram, Email, Slack)
uses this builder so formatting stays consistent.
"""

from datetime import datetime


class MessageBuilder:

    def build(self, signal):
        
        # Format the timestamp - use created_at from signal
        try:
            signal_time = datetime.fromisoformat(signal.created_at)
            timestamp = signal_time.strftime("%d %b %Y • %H:%M:%S")
        except:
            timestamp = "Time unknown"
        
        # Determine emoji based on decision
        emoji_map = {
            "BUY": "🟢",
            "SELL": "🔴",
            "IGNORE": "⚪"
        }
        emoji = emoji_map.get(signal.decision, "•")

        message = f"""{emoji} SGX INSIDER ALERT

┌─ {signal.stock_code} ─────────────────────┐

{signal.company_name}

Director: {signal.director_name}
Transaction: {signal.transaction_type.replace("_", " ").title()}
Decision: {signal.decision}

Confidence: {signal.confidence:.0f}%

{signal.reason}

Announced: {timestamp}

└────────────────────────────────────┘"""

        return message.strip()
