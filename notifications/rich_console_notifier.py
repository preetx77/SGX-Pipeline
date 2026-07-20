"""
Rich Console Notifier

Displays InsiderSignal objects
in a clean human-readable format.
"""


class RichConsoleNotifier:

    def notify(self, signal):

        print()

        print("═" * 70)
        print("🚨 SGX INSIDER SIGNAL")
        print("═" * 70)

        print()

        print(f"Company      : {signal.company_name} ({signal.stock_code})")

        print(f"Director     : {signal.director_name}")

        print()

        print(f"Transaction  : {signal.transaction_type}")

        print(f"Signal       : {signal.signal_type}")

        print(f"Direction    : {signal.direction}")

        print()

        print(f"Importance   : {signal.importance}/10")

        print(f"Confidence   : {signal.confidence:.1f}%")

        print()

        print("Reason")

        print("-" * 70)

        print(signal.reason)

        print()

        print("═" * 70)

        print()