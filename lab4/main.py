import os

from corpus_collector import CorpusCollector
from matcher import levErrorProbability, best10Words


def main():
    corpusFileNames = ['dramat.txt', 'popul.txt', 'proza.txt', 'publ.txt', 'wp.txt']
    corpusPath = (os.path.join('data', fn) for fn in corpusFileNames)

    cc = CorpusCollector()
    for cp in corpusPath:
        cc.update(cp)

    prob = cc.getProbability()
    for wrongWord in getWords():
        bestWord = best10Words(wrongWord, levErrorProbability, prob)
        print(f"Best word: {bestWord}")


def getWords():
    yield 'bende'
    yield 'cut'
    while True:
        inp = input('Get wrong word:\n').lstrip().rstrip().lower()
        if inp:
            yield inp


if __name__ == '__main__':
    main()
