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

        # Format transaction details if available
        shares_str = ""
        if signal.shares:
            shares_str = f"Shares: {signal.shares:,}\n"
        
        price_str = ""
        if signal.price:
            price_str = f"Price: SGD {signal.price:.4f}\n"
        
        value_str = ""
        if signal.value:
            value_str = f"Value: SGD {signal.value:,.2f}\n"

        # Format holdings before/after with % change
        holdings_str = ""
        if signal.direct_interest_before is not None and signal.direct_interest_after is not None:
            before = signal.direct_interest_before
            after = signal.direct_interest_after
            pct_change = ((after - before) / before * 100) if before != 0 else 0
            
            change_indicator = "📈" if pct_change > 0 else "📉" if pct_change < 0 else "➡️"
            holdings_str = f"Holdings: {before:,} → {after:,} {change_indicator} ({pct_change:+.1f}%)\n"

        message = f"""{emoji} SGX INSIDER ALERT

┌─ {signal.stock_code} ─────────────────────┐

{signal.company_name}

Director: {signal.director_name}
Transaction: {signal.transaction_type.replace("_", " ").title()}
Decision: {signal.decision}

{shares_str}{price_str}{value_str}{holdings_str}
Confidence: {signal.confidence:.0f}%

{signal.reason}

Announced: {timestamp}

└────────────────────────────────────┘"""

        return message.strip()
