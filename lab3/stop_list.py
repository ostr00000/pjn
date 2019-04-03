from collections import defaultdict
from operator import itemgetter
import regex as re


class StopList:
    PATTERN = re.compile('\P{L}')

    @staticmethod
    def zero():
        return 0

    def __init__(self, ):
        self.words = defaultdict(self.zero)
        self.excluded: set = None

    def read(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip().lower()
                for word in filter(None, self.PATTERN.split(line)):
                    self.words[word] += 1

    def getSortedWords(self):
        return sorted(self.words.items(), key=itemgetter(1, 0))

    def excludeByFirstN(self, firstN: int):
        sor = self.getSortedWords()
        self.excluded = {k for k, v in sor[-firstN:]}

    def excludeByWordsMargin(self, wordsMargin: int):
        self.excluded = {k for k, v in self.words.items()
                         if v > wordsMargin}
