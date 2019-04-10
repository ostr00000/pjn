from collections import defaultdict
from math import sqrt
from typing import Type, Iterable

import numpy as np
import regex as re

from lab1.metrics import Metric, Euclidean


class NGram:
    LETTERS_PATTERN = re.compile('\P{L}')

    def __init__(self, n: int, onlyLetters=True, processText=False, encoding='iso-8859-1'):
        self.n = n
        self.onlyLetters = onlyLetters
        self.processText = processText
        self.seqCounter = defaultdict(self._zero)
        self.encoding = encoding

        self.vector = None

    @staticmethod
    def _zero():
        return 0.

    def process(self, filenameOrText: str):
        for word in self._wordGenerator(filenameOrText):
            word = word.lower()
            for startIndex in range(1 - self.n, len(word)):
                endIndex = startIndex + self.n
                startIndex = max(0, startIndex)
                seq = word[startIndex:endIndex]
                self.seqCounter[seq] += 1

        if not self.processText:
            print(f"processed {filenameOrText} [{self.n}]")

    def _wordGenerator(self, filenameOrText: str):
        if self.processText:
            if self.onlyLetters:
                yield from filter(None, self.LETTERS_PATTERN.split(filenameOrText))
            else:
                yield from filenameOrText.split()
            return

        with open(filenameOrText, 'r', encoding=self.encoding) as file:
            if self.onlyLetters:
                for line in file:
                    yield from filter(None, self.LETTERS_PATTERN.split(line))
            else:
                for line in file:
                    yield from line.split()

    def distance(self, obj: 'NGram', metricClass: Type[Metric] = Euclidean):
        metric = metricClass()
        allKeys = list(set().union(self.seqCounter.keys(), obj.seqCounter.keys()))
        s1, s2 = self.seqCounter, obj.seqCounter
        s1 = np.array([s1[key] for key in allKeys])
        s2 = np.array([s2[key] for key in allKeys])

        return metric.getDistance(s1, s2)

    def prepareCache(self, possibleKeys: Iterable[str]):
        self.vector = np.array([self.seqCounter[key] for key in possibleKeys])

    def normalize(self):
        total = sqrt(sum(i ** 2 for i in self.seqCounter.values()))
        for k, v in self.seqCounter.items():
            self.seqCounter[k] = v / total
