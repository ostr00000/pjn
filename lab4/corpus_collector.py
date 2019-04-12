from collections import defaultdict

import regex


class CorpusCollector:
    SPLIT_PATTERN: regex.Regex = regex.compile('\P{L}')

    @staticmethod
    def getSmoothingBase():
        return 100000

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
