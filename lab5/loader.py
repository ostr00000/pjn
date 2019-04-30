import os
from cProfile import Profile
from collections import defaultdict

import regex
from pyprof2calltree import visualize

from lab3.stop_list import StopList
from lab5.cache import LocalCache
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

        self._primaryForm = primaryForm
        self._load(path)
        self._primaryForm = None
        print("loaded")

        self._removeHapaxLegomena()
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


def getGraph(loader):
    from graph import GraphModel
    g = GraphModel(loader)
    g.processGraphs(slice(1000))
    return g


def main():
    primaryForm = LocalCache.load('primaryForm', lambda: PrimaryForm(primaryFormPath))
    loader = LocalCache.load('loaderPrimaryForm', lambda: Loader(primaryForm=primaryForm))

    LocalCache.loadGraph('graph2', size=51555)

    # profiler = Profile()
    # runStr = "getGraph(loader)"
    # profiler.runctx(runStr, globals(), locals())
    # visualize(profiler.getstats())

    g = getGraph(loader)


if __name__ == '__main__':
    main()

""" 0 - same process, 00 - primaryForm+scipy 000 - hapaxLegomena
Process \ text: 
    100     1000

000 1.2s    12s
00  2s      20s
0   5s      50s

1   8.2     55.7
2   6.7     32
3   7       24.7
4   7.8     20.3
5   9.3     24
6   10.5    23.3
7   12.4    24.8
8   12.8      26
"""
