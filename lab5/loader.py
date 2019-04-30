import os
from cProfile import Profile
from collections import defaultdict

import regex
from pyprof2calltree import visualize

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
        self.nodelist = sorted(self.words.keys())
        print("sorted")

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


def getGraph(loader):
    from graph import GraphModel
    g = GraphModel(loader)
    g.processGraphs(slice(100))
    return g


def main():
    loader = LocalCache.load('loader', lambda: Loader())
    # LocalCache.loadGraph('graph2', size=1000)

    # profiler = Profile()
    # runStr = "getGraph(loader)"
    # profiler.runctx(runStr, globals(), locals())
    # visualize(profiler.getstats())

    g = getGraph(loader)
    from pympler import asizeof
    print(asizeof.asizeof(g))


if __name__ == '__main__':
    main()

""" 0 - same process
Process \ text: 
    100     1000
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
