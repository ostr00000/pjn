import logging
import os
import random
from pprint import pprint
from typing import List, Tuple

import numpy as np
from gensim.corpora import MmCorpus, WikiCorpus, Dictionary
from gensim.models import KeyedVectors, Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')

logger = logging.getLogger(__name__)

corpusPath = os.path.join('data', 'corpus.save')
modelPath = os.path.join('data', 'w2v.save')
dictPath = os.path.join('data', 'dict.save')


def simple_tokenize():
    pass


def getInputPath() -> str:
    for file in os.scandir(os.path.join('data')):
        if file.name.endswith('.bz2'):
            return file.path
    raise ValueError


class Model:

    def __init__(self):
        self.model = self._getModel()
        self.tokenMap = self._getDictionary().token2id

    @staticmethod
    def _getModel() -> KeyedVectors:
        try:
            w2v = KeyedVectors.load(modelPath)
        except FileNotFoundError:
            Model._getCorpus()
            w2v = Word2Vec(corpus_file=corpusPath, workers=7, window=5,
                           size=300, iter=15, sg=1)
            w2v.wv.save(modelPath)
        return w2v

    @staticmethod
    def _getCorpus():
        try:
            wc = MmCorpus(corpusPath)
        except FileNotFoundError:
            wc = WikiCorpus(getInputPath())
            wc.dictionary.save(dictPath)
            MmCorpus.serialize(corpusPath, wc)
        return wc

    @staticmethod
    def _getDictionary() -> Dictionary:
        obj = Dictionary.load(dictPath)
        if isinstance(obj, Dictionary):
            return obj
        raise ValueError

    def exampleSimilarity(self):
        def getRandom():
            return str(random.randint(0, len(self.tokenMap)))

        def getVector():
            while True:
                num = getRandom()
                try:
                    return self.model[num]
                except KeyError:
                    pass

        vectors = []
        for _ in range(5):
            a = getVector()
            b = getVector()
            vectors.append(a - b)

        self.printSimilarity(vectors)

    def printMostSimilar(self, positive=(), negative=()):
        if isinstance(positive, str):
            positive = (positive,)
        if isinstance(negative, str):
            negative = (negative,)

        sim = self.model.most_similar(
            positive=[str(self.tokenMap[t]) for t in positive],
            negative=[str(self.tokenMap[t]) for t in negative],
            topn=1000,
        )

        rev = {str(v): k for k, v in self.tokenMap.items()}
        newSim = [(rev[k], v) for k, v in sim]
        pprint(newSim)

    @staticmethod
    def printSimilarity(vectors):
        sim = (cosine_similarity(vectors, vectors) + 1) / 2
        print(sim)
        print(np.sum(sim))

    def checkRelation(self, words: List[Tuple[str, str]]):
        vectors = []

        for wordA, wordB in words:
            wordIdA = str(self.tokenMap[wordA])
            wordIdB = str(self.tokenMap[wordB])
            try:
                difVector = self.model[wordIdA] - self.model[wordIdB]
            except KeyError:
                logging.error(f"At least one key not found ({wordA}, {wordB})")
            else:
                vectors.append(difVector)

        self.printSimilarity(vectors)


def main():
    model = Model()
    model.checkRelation([
        ("król", "królowa"),
        ("mężczyzna", "kobieta"),
    ])
    model.checkRelation([
        ('atakować', 'atakował'),
        ('zrobić', 'zrobił'),
        ('kupić', 'kupił'),
        ('malować', 'namalował'),
        ('tworzyć', 'stworzył'),
    ])
    model.exampleSimilarity()
    model.printMostSimilar(positive=('król', 'kobieta'), negative='mężczyzna')
    model.printMostSimilar(positive='mysz')


if __name__ == '__main__':
    """
    https://dumps.wikimedia.org/plwiki/
    https://dumps.wikimedia.org/plwiki/20190601/plwiki-20190601-pages-articles-multistream.xml.bz2
    """
    main()
