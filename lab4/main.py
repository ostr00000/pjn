import math
import os
from collections import defaultdict
from typing import Dict, Callable

import regex


def levMetric(xStr: str, yStr: str):
    arr = list(range(len(xStr) + 1))

    for left, y in enumerate(yStr, start=1):
        skew = left - 1
        for j, x in enumerate(xStr, start=1):
            upper = arr[j]
            eq = 1 if x != y else 0
            newVal = min((upper + 1, skew + eq, left + 1))
            skew = upper
            left = arr[j] = newVal

    result = arr[-1]
    return result


assert levMetric('biurko', 'pióro') == 3


class CorpusCollector:
    SPLIT_PATTERN: regex.Regex = regex.compile('\P{L}')

    @staticmethod
    def getSmoothingBase():
        return 1

    def __init__(self):
        self.wordsFrequency = defaultdict(self.getSmoothingBase)
        self.totalProcessedWords = 0

    def update(self, filename):
        with open(filename) as file:
            for line in file:
                words = filter(None, self.SPLIT_PATTERN.split(line.lower()))
                for word in words:
                    self.wordsFrequency[word] += 1
                    self.totalProcessedWords += 1

    def getProbability(self):
        den = self.totalProcessedWords + self.getSmoothingBase() * len(self.wordsFrequency)
        return {word: freq / den for word, freq in self.wordsFrequency.items()}


def bestCorrectWord(errorWord: str, fun: Callable[[str, str], float],
                    possibleWords: Dict[str, float]) -> float:
    best = 0, None
    for correctWord, freq in possibleWords.items():
        prob = fun(errorWord, correctWord) / max(1, 100 * abs(len(errorWord) - len(correctWord)))
        val = prob * freq
        if val > best[0]:
            best = val, correctWord

    return best[1]


def errorProbability(xStr: str, yStr: str):
    return 1 - (levMetric(xStr, yStr) / max(len(xStr), len(yStr)))


def main():
    corpusFileNames = ['dramat.txt', 'popul.txt', 'proza.txt', 'publ.txt', 'wp.txt']
    corpusPath = (os.path.join('data', fn) for fn in corpusFileNames)

    cc = CorpusCollector()
    for cp in corpusPath:
        cc.update(cp)

    prob = cc.getProbability()
    while True:
        wrongWord = input('Get wrong word:\n').lstrip().rstrip()
        # wrongWord = 'bende'
        bestWord = bestCorrectWord(wrongWord, errorProbability, prob)
        print(f"Best word: {bestWord}")


if __name__ == '__main__':
    main()
