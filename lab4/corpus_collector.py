from collections import defaultdict

import regex


class CorpusCollector:
    SPLIT_PATTERN: regex.Regex = regex.compile('\P{L}')

    @staticmethod
    def getSmoothingBase():
        return 50_000

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


"""
bende
10_000
Best word: ['nie', 'się', 'będę', 'wende', 'mende', 'bene', 'będą', 'bandę', 'będze', 'będzie']
20_000
Best word: ['będę', 'nie', 'wende', 'mende', 'bene', 'bandę', 'będze', 'będą', 'będ', 'będzie']
50_000
Best word: ['będę', 'wende', 'mende', 'bene', 'bandę', 'będze', 'będą', 'będ', 'rendez', 'bunder']

cut
10_000
Best word: ['się', 'nie', 'ciut', 'cud', 'but', 'hut', 'nut', 'cum', 'cgt', 'cuć']
20_000
Best word: ['ciut', 'cud', 'but', 'hut', 'nut', 'cum', 'cgt', 'cuć', 'cdt', 'aut']
50_000
Best word: ['ciut', 'cud', 'but', 'hut', 'nut', 'cum', 'cgt', 'cuć', 'cdt', 'aut']
"""
