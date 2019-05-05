import os
from collections import defaultdict

import regex

from lab3.stop_list import StopList
from primary_form import PrimaryForm

dataPath = os.path.join('data', 'pap.txt')
primaryFormPath = os.path.join('data', 'odm.txt')


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

        self._removeHapaxLegomena()
        self.removeCommon()
        self._common = None
        self._useStopList()
        print("stopListed")

        self.nodelist = sorted(self._words.keys())
        self._words = None
        print("sorted")  # 250_000 -> 40_600 -> 29_700

    def _load(self, path):
        lastData = []
        with open(path, 'r') as file:
            for line in file:
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

    def _removeHapaxLegomena(self):
        self._words = {k: v for k, v in self._words.items() if v > 1}

    def _useStopList(self):
        sl = StopList()
        sl.words = self._words
        sl.excludeByWordsMargin(1000)
        for ex in sl.excluded:
            del self._words[ex]

        for i, note in enumerate(self.data):
            self.data[i] = [word for word in note if word not in sl.excluded]

    def removeCommon(self):
        total = len(self.data)
        factor = 0.7 * total
        excluded = [key for key, val in self._common.items() if val > factor]
        for ex in excluded:
            del self._words[ex]

        for i, note in enumerate(self.data):
            self.data[i] = [word for word in note if word not in excluded]
