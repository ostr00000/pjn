import math
from typing import Dict

import numpy as np
from scipy import sparse
from scipy.sparse import vstack

from lab5.loader import Loader
from util import LogIter


class TfidfModel:

    def __init__(self, loader: Loader):
        self.loader = loader
        self.vectors = None

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

    def _getDocumentFrequency(self, word2Index: Dict[str, int]):
        documentFrequency = np.full(len(self.loader.nodelist), fill_value=1)
        for note in self.loader.data:
            for word in set(note):
                documentFrequency[word2Index[word]] += 1

        return np.log(len(self.loader.data) / documentFrequency)

    def calcVector(self):
        word2Index = {word: i for i, word in enumerate(self.loader.nodelist)}
        documentFrequency = self._getDocumentFrequency(word2Index)
        self.vectors = []

        allWordsNum = len(self.loader.nodelist)
        for note in LogIter(self.loader.data):
            termFrequency = np.zeros(allWordsNum)
            for word in note:
                termFrequency[word2Index[word]] += 1

            termFrequency *= documentFrequency
            self.vectors.append(sparse.csr_matrix(termFrequency))

        self.vectors = vstack(self.vectors)

    def __str__(self):
        return "Tf_idf"
