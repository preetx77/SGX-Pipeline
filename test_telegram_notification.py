"""
Test Telegram Notification with a Simulated MARKET_PURCHASE Signal
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("TELEGRAM NOTIFICATION TEST")
print("=" * 70)

# Create a test signal that SHOULD trigger notification
from models.insider_signal import InsiderSignal

test_signal = InsiderSignal(
    announcement_id="TEST_TELEGRAM_001",
    company_name="HYPHENS PHARMA INTERNATIONAL LIMITED",
    stock_code="1J5",
    director_name="Lim See Wah",
    signal=True,  # THIS IS KEY - signal must be True
    signal_type="INSIDER_BUY",
    direction="BULLISH",
    importance=5,
    confidence=95.0,
    reason="Director purchased shares through the open market.",
    transaction_type="MARKET_PURCHASE",
    shares=100000,
    price=0.50,
    value=50000.0,
    decision="BUY"
)

print("\n✓ Created test signal:")
print(f"  Company: {test_signal.company_name}")
print(f"  Director: {test_signal.director_name}")
print(f"  Transaction: {test_signal.transaction_type}")
print(f"  Signal: {test_signal.signal}")
print(f"  Should notify: {'YES' if test_signal.signal else 'NO'}")

# Build the message
print("\n[1] Building Telegram message...")
from notifications.message_builder import MessageBuilder
builder = MessageBuilder()

message = builder.build(test_signal)
print("✓ Message built:")
print("-" * 70)
print(message)
print("-" * 70)

# Send to Telegram
print("\n[2] Sending to Telegram...")
from notifications.telegram_notifier import TelegramNotifier

try:
    notifier = TelegramNotifier()
    print("✓ Notifier initialized")
    
    # This will actually send the message!
    notifier.notify(test_signal)
    print("✓ Message sent!")
    
    print("\n" + "=" * 70)
    print("✅ TELEGRAM NOTIFICATION SENT SUCCESSFULLY")
    print("=" * 70)
    print("\nCheck your Telegram app for the message!")
    
except Exception as e:
    print(f"❌ Failed to send: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
