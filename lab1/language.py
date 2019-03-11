import os
import re
import time
from collections import defaultdict
from typing import Iterator, Tuple, Dict, Type

from decorator import decorator

from metrics import Metric
from ngram import NGram


@decorator
def timeDec(fun, *args, **kwargs):
    start = time.time()
    try:
        return fun(*args, **kwargs)
    finally:
        end = time.time()
        total_time = end - start
        msg = "{name}, execute time:{time:.4f}s" \
            .format(name=fun.__name__, time=total_time)
        print(msg)


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
    def dataFileNameGenerator(path: str) -> Iterator[str]:
        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                yield filename

    @timeDec
    def process(self):
        for filename in self.dataFileNameGenerator(self.dataFolder):
            match = self.FILE_PATTERN.match(filename)
            if not match:
                raise TypeError(f"Unexpected file format '{filename}'")

            filePath = os.path.join(self.dataFolder, filename)
            for nGram in self.languages[match.group(1)]:
                nGram.process(filePath)

    def normalize(self):
        for nGrams in self.languages.values():
            for nGram in nGrams:
                nGram.normalize()

    def guessLanguage(self, text: str, metric: Type[Metric]) -> Dict[str, Dict[int, float]]:
        testNGrams = self.createNGrams()
        for testNGram in testNGrams:
            testNGram.processText = True
            testNGram.process(text)
            testNGram.normalize()

        lang2N2Val = defaultdict(dict)

        for langName, nGrams in self.languages.items():
            for g1, g2 in zip(nGrams, testNGrams):
                assert g1.n == g2.n
                dist = g1.distance(g2, metric)
                lang2N2Val[langName][g1.n] = dist

        # weights = sorted(lang2N2Val.items(), key=lambda kv: )kv[1]
        return lang2N2Val
