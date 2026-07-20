import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from classifiers.director_dealings_classifier import DirectorDealingsClassifier
classifier = DirectorDealingsClassifier()

examples = [

    (
        "Securities via market transaction\nAcquisition",
        "MARKET_PURCHASE"
    ),

    (
        "Securities via market transaction\nDisposal",
        "MARKET_SELL"
    ),

    (
        "Bonus Issue",
        "BONUS_ISSUE"
    ),

    (
        "Rights Issue",
        "RIGHTS_ISSUE"
    ),

    (
        "Employee share option",
        "OPTION_EXERCISE"
    )

]

for text, expected in examples:

    result = classifier.classify(text)

    print(f"{expected:20} -> {result}")