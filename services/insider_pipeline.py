from extractors.insider.director_dealings_extractor import (
    DirectorDealingsExtractor,
)

from services.signals.insider_signal_generator import (
    InsiderSignalGenerator,
)

from notifications.telegram_notifier import (
    TelegramNotifier,
)


class InsiderPipeline:

    def __init__(self):

        self.extractor = DirectorDealingsExtractor()
        self.generator = InsiderSignalGenerator()
        self.notifier = TelegramNotifier()

    def process(
        self,
        announcement,
        documents,
    ):
        print("Documents recieved :", len(documents))

        if not documents:
            return

        document = documents[0]

        dealing = self.extractor.extract(
            announcement,
            document,
        )

        signal = self.generator.generate(
            dealing
        )

        if signal.signal:
            self.notifier.notify(signal)