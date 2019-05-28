from collections import defaultdict
from typing import IO, Union, Tuple

import numpy as np
import regex


class Author:
    SPLIT_PATTERN: regex.Regex = regex.compile('\P{L}')
    discount = 0.9
    SENTENCE_PATTERN: regex.Regex = regex.compile(r' *[\.\?!][\'"\)\]]* *')

    @staticmethod
    def zero():
        return 0.

    @staticmethod
    def dictZero():
        return defaultdict(Author.zero)

    def __init__(self, name=''):
        self.name = name
        self.gram = defaultdict(Author.dictZero)

    @staticmethod
    def sentenceGen(file: IO):
        data = file.read().lower()
        sentences = Author.SENTENCE_PATTERN.split(data)
        yield from sentences

    def loadBooks(self, bookFile: IO):
        for sentence in self.sentenceGen(bookFile):
            words = list(filter(None, self.SPLIT_PATTERN.split(sentence)))
            words = ' '.join(words)
            if len(words) < 2:
                continue
            if len(words) >= 3:
                w1, w2, *wordsIter = words
                for w3 in wordsIter:
                    self.gram[w1, w2][w3] += 1
                    w1, w2 = w2, w3

            w1, *wordsIter = words
            for w2 in wordsIter:
                self.gram[(w1,)][w2] += 1
                w1 = w2

            for w1 in words:
                self.gram[()][w1] += 1

    def calcProbability(self):
        for val in self.gram.values():
            s = sum(val.values())
            for k, v in val.items():
                val[k] = v / s * self.discount

    def getProbability(self, prev: Union[Tuple[str, str], Tuple[str]], cur: str):
        pre = self.gram.get(prev, None)
        if pre is not None:
            p = pre.get(cur, None)
            if p is not None:
                return p  # P(cur|prev)

        if len(prev) > 1:
            p = self.getProbability(prev[1:], cur)
            if p > 0:
                bow = self.backOfWeight(prev)
                return bow * p  # a1 * P(cur|prev-1)

        return self.gram[()][cur]  # a2 * P(cur)

    def backOfWeight(self, val: Union[Tuple[str, str], Tuple[str]]):
        possibilities = self.gram[val]
        nom, den = 0, 0
        for pos in possibilities:
            nom += self.getProbability(val, pos)

        assert nom != 1
        if nom == 0:
            return nom

        val = val[1:]
        possibilities = self.gram[val]
        for pos in possibilities:
            den += self.getProbability(val, pos)

        assert den != 0
        return (1 - nom) / den

    def printProb(self, s):
        pr = self.getProbability((s[0], s[1]), s[2])
        print(s, pr)

    def sentenceProb(self, sent):
        totalProb = 0
        for i in range(len(sent) - 2):
            t = tuple(sent[i:i + 2])
            t2 = sent[i + 2]
            p = self.getProbability(t, t2)
            if not p:
                totalProb += 10
                continue

            log = -np.log10(p)
            totalProb += log
        return totalProb


def test():
    import io

    s = io.StringIO('w e a. w e a. w e b. e c. i j k.')
    a = Author()
    a.loadBooks(s)
    a.calcProbability()

    a.printProb('wea')
    a.printProb('web')
    a.printProb('wec')

    a.printProb('ijk')
    a.printProb('qjk')
    a.printProb('qqk')
    a.printProb('qqq')


"""
wea 0.6
web 0.3
wec 0.025000000000000022
ijk 0.9
qjk 1.0
qqk 0
qqq 0
"""
