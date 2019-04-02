import os
import re
from operator import itemgetter
from collections import defaultdict

path = os.path.join('data', 'lines.txt')


class StopList:
    PATTERN = re.compile('[\'" .,:;]+')

    def __init__(self, ):
        self.words = defaultdict(lambda: 0)
        self.excluded: set = None

    def read(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                for word in filter(None, self.PATTERN.split(line)):
                    self.words[word] += 1

    def excludeByFirstN(self, firstN: int):
        sor = sorted(self.words.items(), key=itemgetter(1, 0))
        self.excluded = {k for k, v in sor[-firstN:]}

    def excludeByWordsMargin(self, wordsMargin: int):
        self.excluded = {k for k, v in self.words.items()
                         if v > wordsMargin}


class Classification:
    pass


def main():
    c = StopList()
    c.read(path)
    c.excludeByFirstN(100)
    

if __name__ == '__main__':
    main()
