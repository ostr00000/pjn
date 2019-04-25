import os
from collections import defaultdict

import regex

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


if __name__ == '__main__':
    loader = Loader()
    print(loader.data[:10])
