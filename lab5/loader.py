import os
from collections import defaultdict

import regex
from decorator import decorator

from lab3.stop_list import StopList
from primary_form import PrimaryForm
from util import LogIter

dataPath = os.path.join('data', 'pap.txt')
primaryFormPath = os.path.join('data', 'odm.txt')


@decorator
def excludedPrintDec(fun, *args, **kwargs):
    self, *_ = args
    before = len(self._excluded)
    ret = fun(*args, **kwargs)
    after = len(self._excluded)
    print(fun.__name__ + f" {after-before}")
    return ret


class Loader:
    SPLIT_PATTERN: regex.Regex = regex.compile('\P{L}')

    @staticmethod
    def zero():
        return 0

    def __init__(self, path=dataPath, primaryForm: PrimaryForm = None):
        self.data = []
        self._words = defaultdict(self.zero)
        self._common = defaultdict(self.zero)

        self._primaryForm = primaryForm
        self._load(path)
        self._primaryForm = None
        print("loaded")

        self._excluded = []
        self._removeHapaxLegomena()
        self._removeCommon()
        self._common = None
        self._useStopList()
        self._filterExcluded()
        self._excluded = None
        print("stopListed")

        self.nodelist = sorted(self._words.keys())
        self._words = None
        print("sorted")  # 250_000 -> 40_600 -> 29_700

    def _load(self, path):
        lastData = []
        with open(path, 'r') as file:
            for line in LogIter(file, 10000):  # file has ~ 424_000 lines
                if line.startswith('#'):
                    self.data.append(lastData)
                    for common in set(lastData):
                        self._common[common] += 1
                    lastData = []
                    continue

                line = line.lstrip().rstrip().lower()
                line = list(filter(None, self.SPLIT_PATTERN.split(line)))
                if self._primaryForm:
                    line = list(map(self.getPrimaryForm, line))
                    line = list(filter(None, line))
                for word in line:
                    self._words[word] += 1
                lastData.extend(line)

        self.data.pop(0)
        self.data.append(lastData)
        for common in set(lastData):
            self._common[common] += 1

    def getPrimaryForm(self, word):
        try:
            return self._primaryForm.dictionary[word]
        except KeyError:
            return None

    @excludedPrintDec
    def _removeHapaxLegomena(self):
        self._excluded.extend([k for k, v in self._words.items() if v <= 1])

    @excludedPrintDec
    def _useStopList(self):
        sl = StopList()
        sl.words = self._words
        sl.excludeByWordsMargin(1000)
        self._excluded.extend(sl.excluded)

    @excludedPrintDec
    def _removeCommon(self):
        total = len(self.data)
        factor = 0.5 * total
        excluded = [key for key, val in self._common.items() if val > factor]
        self._excluded.extend(excluded)

    @excludedPrintDec
    def _filterExcluded(self):
        self._excluded = set(self._excluded)

        for i, note in enumerate(self.data):
            self.data[i] = [word for word in note if word not in self._excluded]

        for ex in self._excluded:
            del self._words[ex]
