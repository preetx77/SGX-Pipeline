"""
Base Extractor : Every document extractor inherits from this class.
"""

from abc import ABC, abstractmethod

class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, document):
        """
        Extract structured information from a Document.
        """
        pass