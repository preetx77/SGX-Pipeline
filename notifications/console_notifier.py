from notifications.message_builder import MessageBuilder


class RichConsoleNotifier:

    def __init__(self):

        self.builder = MessageBuilder()

    def notify(self, signal):

        print()

        print(self.builder.build(signal))

        print()