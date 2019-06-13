import logging
import os
import random
from pprint import pprint
from typing import List, Tuple

import gensim.utils
import numpy as np
import regex as re
from gensim.corpora import MmCorpus, WikiCorpus, Dictionary
from gensim.corpora.wikicorpus import TOKEN_MAX_LEN, TOKEN_MIN_LEN
from gensim.models import KeyedVectors, Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')

logger = logging.getLogger(__name__)
np.set_printoptions(precision=3)

corpusPath = os.path.join('data', 'corpus.save')
modelPath = os.path.join('data', 'w2v.save')
dictPath = os.path.join('data', 'dict.save')

POLISH_WORDS = re.compile(r'^[aąbcćdeęfghijklłmnńoóprsśtuwyzźż]+$', re.UNICODE)


def tokenize(content, token_min_len=TOKEN_MIN_LEN, token_max_len=TOKEN_MAX_LEN, lower=True):
    return [gensim.utils.to_unicode(token)
            for token in gensim.utils.tokenize(content, lower=lower, errors='ignore')
            if (token_min_len <= len(token) <= token_max_len
                and not token.startswith('_')
                and bool(POLISH_WORDS.search(token)))]


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
            wc = WikiCorpus(getInputPath(), tokenizer_func=tokenize)
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
            topn=50,
        )

        rev = {str(v): k for k, v in self.tokenMap.items()}
        newSim = [(rev[k], v) for k, v in sim]
        pprint(newSim)

    @staticmethod
    def printSimilarity(vectors):
        sim = (cosine_similarity(vectors, vectors) + 1) / 2
        print(sim)
        num = (len(vectors) ** 2 - len(vectors)) / 2
        avr = ((np.sum(sim) - len(vectors)) / 2) / num
        print(f"Avr under diagonal: {avr}")

    def checkRelation(self, relationName, words: List[Tuple[str, str]]):
        print()
        print(f"Relation: {relationName}")
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
    model.checkRelation("czas teraźniejszy - czas przeszły", [
        ('atakować', 'atakował'),
        ('zrobić', 'zrobił'),
        ('kupić', 'kupił'),
        ('malować', 'malował'),
        ('tworzyć', 'tworzył'),
    ])
    model.checkRelation("mianownik - dopełniacz", [
        ("król", "króla"),
        ("polska", "polski"),
        ("dom", "domu"),
        ("model", "modelu"),
        ("wieża", "wieży"),
    ])
    model.checkRelation("liczba pojendyńcza - liczb mnoga", [
        ("towar", "towary"),
        ("zamek", "zamki"),
        ("dom", "domy"),
        ("krzesło", "krzesła"),
        ("samochód", "samochody"),
    ])

    model.checkRelation("mężczyzna  - kobieta", [
        ("król", "królowa"),
        ("mężczyzna", "kobieta"),
        ("brat", "siostra"),
        ("wujek", "ciocia"),
        ("dziadek", "babcia"),
    ])
    model.checkRelation("państwo - stolica", [
        ("polska", "warszawa"),
        ("niemcy", "berlin"),
        ("rosja", "moskwa"),
        ("włochy", "rzym"),
        ("hiszpania", "madryt"),
    ])
    model.checkRelation("postać - funkcja/zawód", [
        ("chrobry", "król"),
        ("poniatowski", "król"),
        ("chopin", "pianista"),
        ("mickiewicz", "pisarz"),
        ("sienkiewicz", "pisarz"),
    ])

    # model.exampleSimilarity()
    # model.printMostSimilar(positive=('król', 'kobieta'), negative='mężczyzna')
    # model.printMostSimilar(positive='mysz')


if __name__ == '__main__':
    """
    https://dumps.wikimedia.org/plwiki/
    https://dumps.wikimedia.org/plwiki/20190601/plwiki-20190601-pages-articles-multistream.xml.bz2
    """
    main()
