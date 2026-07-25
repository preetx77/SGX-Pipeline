import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.insider_signal_repository import InsiderSignalRepository
from models.insider_signal import InsiderSignal
from datetime import datetime

repo = InsiderSignalRepository()

signal = InsiderSignal(
    announcement_id="TEST123456",
    company_name="TEST COMPANY",
    stock_code="TEST",
    director_name="John Doe",
    signal=True,
    signal_type="BUY",
    direction="BULLISH",
    importance=5,
    confidence=95.5,
    reason="Repository Test",
    transaction_type="MARKET_PURCHASE",
    shares=10000,
    price=1.25,
    value=12500,
    decision="BUY",
    market_impact="Positive",
    summary="Testing repository insert.",
    created_at=datetime.now().isoformat()
)

repo.insert(signal)

print("Insert successful.")