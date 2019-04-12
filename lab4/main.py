import os

from corpus_collector import CorpusCollector
from matcher import bestCorrectWord, levErrorProbability


def main():
    corpusFileNames = ['dramat.txt', 'popul.txt', 'proza.txt', 'publ.txt', 'wp.txt']
    corpusPath = (os.path.join('data', fn) for fn in corpusFileNames)

    cc = CorpusCollector()
    for cp in corpusPath:
        cc.update(cp)

    prob = cc.getProbability()
    while True:
        wrongWord = input('Get wrong word:\n').lstrip().rstrip().lower()
        if wrongWord:
            bestWord = bestCorrectWord(wrongWord, levErrorProbability, prob)
            print(f"Best word: {bestWord}")


if __name__ == '__main__':
    main()
