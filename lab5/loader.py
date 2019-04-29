import os
from collections import defaultdict

import regex

from lab3.stop_list import StopList
from lab5.cache import LocalCache

dataPath = os.path.join('data', 'pap.txt')


class Loader:
    SPLIT_PATTERN: regex.Regex = regex.compile('\P{L}')

    @staticmethod
    def zero():
        return 0

    def __init__(self, path=dataPath):
        self.data = []
        self.words = defaultdict(self.zero)
        self._load(path)
        print("loaded")
        self._useStopList()
        print("stopListed")
        self.word2index = {w: i for i, w in enumerate(self.words)}

    def _load(self, path):
        lastData = []
        with open(path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    self.data.append(lastData)
                    lastData = []
                    continue

                line = line.lstrip().rstrip().lower()
                line = list(filter(None, self.SPLIT_PATTERN.split(line)))
                for word in line:
                    self.words[word] += 1
                lastData.extend(line)

        self.data.pop(0)
        self.data.append(lastData)

    def _useStopList(self):
        sl = StopList()
        sl.words = self.words
        sl.excludeByWordsMargin(1000)
        for ex in sl.excluded:
            del self.words[ex]

        for i, note in enumerate(self.data):
            self.data[i] = [word for word in note if word not in sl.excluded]


def main():
    loader = LocalCache.load('loader', lambda: Loader())
    LocalCache.loadGraph('graph2', size=100)


if __name__ == '__main__':
    main()
