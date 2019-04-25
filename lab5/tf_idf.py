import math

from lab5.loader import Loader


class TfidfModel:

    def __init__(self, loader: Loader):
        self.loader = loader

    def _tf(self, term: str, documentId: int):
        doc = self.loader.data[documentId]
        termOccurrences = sum(1 for word in doc if word == term)
        return termOccurrences

    def _idf(self, term: str):
        n = len(self.loader.data)
        termOccurrence = sum(1 for text in self.loader.data if term in text)
        return math.log(n / (termOccurrence + 1))

    def getWeight(self, term: str, documentId: int):
        return self._tf(term, documentId) * self._idf(term)
