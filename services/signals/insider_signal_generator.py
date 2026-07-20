"""
Insider Signal Generator

Converts a DirectorDealing into an
investment signal.
"""

from models.insider_signal import InsiderSignal


class InsiderSignalGenerator:

    def generate(self, dealing):

        transaction = dealing.transaction_type

        signal = False
        direction = "NEUTRAL"
        signal_type = "INFORMATION"
        confidence = self.confidence(dealing)
        reason = "No meaningful insider signal."

        if transaction == "MARKET_PURCHASE":

            signal = True
            direction = "BULLISH"
            signal_type = "INSIDER_BUY"

            reason = (
                "Director purchased shares "
                "through the open market."
            )

        elif transaction == "MARKET_SELL":

            signal = True
            direction = "BEARISH"
            signal_type = "INSIDER_SELL"

            reason = (
                "Director sold shares "
                "through the open market."
            )

        elif transaction == "BONUS_ISSUE":

            signal = False
            signal_type = "BONUS"

            reason = (
                "Shares received via bonus issue."
            )

        elif transaction == "RIGHTS_ISSUE":

            signal = False
            signal_type = "RIGHTS"

            reason = (
                "Shares received through a rights issue."
            )

        elif transaction == "SHARE_AWARD":

            signal = False
            signal_type = "SHARE_AWARD"

            reason = (
                "Shares granted as compensation."
            )

        elif transaction == "OPTION_EXERCISE":

            signal = True
            direction = "BULLISH"
            signal_type = "OPTION_EXERCISE"

            reason = (
                "Director exercised employee share options."
            )

        return InsiderSignal(

            company_name=dealing.company_name,

            stock_code=dealing.stock_code,

            director_name=dealing.director_name,

            signal=signal,

            signal_type=signal_type,

            direction=direction,

            importance=dealing.importance,

            confidence=confidence,

            reason=reason,

            transaction_type=transaction,

            shares=dealing.shares,

            price=dealing.price,

            value=dealing.value,
        )

    def confidence(self, dealing):

        if dealing.transaction_type == "UNKNOWN":
            return 40.0

        if dealing.director_name is None:
            return 60.0

        if dealing.shares is None:
            return 75.0

        return 98.0