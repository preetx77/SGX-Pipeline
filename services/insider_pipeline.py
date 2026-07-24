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

    def process(self, announcement, attachments):
        print("Inside pipeline:", id(attachments), len(attachments))

    def process(
        self,
        announcement,
        downloaded_documents,
    ):
        print(">>> InsiderPipeline.process() called")
        print("Type:", type(downloaded_documents))
        print("Length:", len(downloaded_documents))
        print("Value:", downloaded_documents)

        if not downloaded_documents:
            return

        document = downloaded_documents[0]

        dealing = self.extractor.extract(
            announcement,
            document,
        )

        signal = self.generator.generate(
            dealing
        )

        if signal.signal:

            self.notifier.notify(signal)