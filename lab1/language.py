import operator
import os
import pickle
import re
from collections import defaultdict, OrderedDict
from typing import Iterator, Tuple, Dict, Type

from metrics import Metric, ALL_METRIC
from ngram import NGram


class LanguageManager:
    FILE_PATTERN = re.compile('(\D+)(\d+)')

    def __init__(self, minN=1, maxN=4, dataFolder: str = 'data'):
        self._minN = minN
        self._maxN = maxN
        self.dataFolder = dataFolder
        self.languages = defaultdict(self.createNGrams)

    def createNGrams(self) -> Tuple[NGram]:
        return tuple(NGram(i) for i in range(self._minN, self._maxN))

    @staticmethod
    def getManager(filename) -> 'LanguageManager':
        try:
            with open(filename, 'rb') as f:
                manager = pickle.load(f)
        except FileNotFoundError:
            manager = LanguageManager()
            manager.process()
            manager.normalize()
            with open(filename, 'wb') as f:
                pickle.dump(manager, f)
        return manager

    def process(self):
        for filename in self.dataFileNameGenerator(self.dataFolder):
            match = self.FILE_PATTERN.match(filename)
            if not match:
                raise TypeError(f"Unexpected file format '{filename}'")

            filePath = os.path.join(self.dataFolder, filename)
            for nGram in self.languages[match.group(1)]:
                nGram.process(filePath)

    @staticmethod
    def dataFileNameGenerator(path: str) -> Iterator[str]:
        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                yield filename

    def normalize(self):
        for nGrams in self.languages.values():
            for nGram in nGrams:
                nGram.normalize()

    def guessLanguage(self, text: str):
        testNGrams = self.getTestNGrams(text)

        retOriginal = {}
        retWeight = {}
        predictedLang = set()
        for metric in ALL_METRIC:
            result = self.checkInMetric(testNGrams, metric)
            retOriginal[metric] = result

            # apply weights
            weightResults = {}
            for lang, nGrams in result.items():
                weightResult = 0
                for nGram, value in nGrams.items():
                    weightResult += 1 * value
                weightResults[lang] = weightResult

            sortedResultList: list = sorted(weightResults.items(), key=operator.itemgetter(1))
            sortedResult = OrderedDict(sortedResultList)
            retWeight[metric] = sortedResult

            predictedLang.add(next(iter(sortedResult)))

        return retOriginal, retWeight, predictedLang

    def getTestNGrams(self, text):
        testNGrams = self.createNGrams()
        for testNGram in testNGrams:
            testNGram.processText = True
            testNGram.process(text)
            testNGram.normalize()
        return testNGrams

    def checkInMetric(self, testNGrams, metric: Type[Metric]) -> Dict[str, Dict[int, float]]:
        lang2N2Val = defaultdict(dict)

        for langName, nGrams in self.languages.items():
            for g1, g2 in zip(nGrams, testNGrams):
                assert g1.n == g2.n
                dist = g1.distance(g2, metric)
                lang2N2Val[langName][g1.n] = dist

        return lang2N2Val
