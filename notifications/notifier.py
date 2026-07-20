from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def notify(self, event):

        pass