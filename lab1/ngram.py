from collections import defaultdict
from math import sqrt
from typing import Type

import regex as re

from metrics import Metric, Euclidean


class NGram:
    LETTERS_PATTERN = re.compile('\P{L}')

    def __init__(self, n: int, onlyLetters=True, processText=False):
        self.n = n
        self.onlyLetters = onlyLetters
        self.processText = processText
        self.seqCounter = defaultdict(self._zero)

    @staticmethod
    def _zero():
        return 0.

    def process(self, filenameOrText: str):
        for word in self._wordGenerator(filenameOrText):
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

        with open(filenameOrText, 'r', encoding='iso-8859-1') as file:
            if self.onlyLetters:
                for line in file:
                    yield from filter(None, self.LETTERS_PATTERN.split(line))
            else:
                for line in file:
                    yield from line.split()

    def distance(self, obj: 'NGram', metricClass: Type[Metric] = Euclidean):
        metric = metricClass()
        for key in set().union(self.seqCounter.keys(), obj.seqCounter.keys()):
            metric.addPair(self.seqCounter[key], obj.seqCounter[key])

        return metric.getResult()

    def normalize(self):
        total = sqrt(sum(i ** 2 for i in self.seqCounter.values()))
        for k, v in self.seqCounter.items():
            self.seqCounter[k] = v / total
