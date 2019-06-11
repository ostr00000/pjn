import logging
import os
import random
from pprint import pprint
from typing import List, Tuple, Dict

import numpy as np
from gensim.corpora import WikiCorpus, MmCorpus, Dictionary
from gensim.models import Word2Vec, KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')

corpusPath = os.path.join('data', 'corpus.save')
modelPath = os.path.join('data', 'w2v.save')
dictPath = os.path.join('data', 'dict.save')


def getInputPath() -> str:
    for file in os.scandir(os.path.join('data')):
        if file.name.endswith('.bz2'):
            return file.path
    raise ValueError


def getCorpus():
    try:
        wc = MmCorpus(corpusPath)
    except FileNotFoundError:
        wc = WikiCorpus(getInputPath())
        wc.dictionary.save(dictPath)
        MmCorpus.serialize(corpusPath, wc)
    return wc


def getModel() -> KeyedVectors:
    try:
        w2v = KeyedVectors.load(modelPath)
    except FileNotFoundError:
        wc = getCorpus()
        w2v = Word2Vec(corpus_file=corpusPath, workers=7, window=5,
                       size=100, iter=1, sg=0)
        w2v.wv.save(modelPath)
    return w2v


def loadDict() -> Dictionary:
    obj = Dictionary.load(dictPath)
    if isinstance(obj, Dictionary):
        return obj
    raise ValueError


def printSimilarity(vectors):
    sim = (cosine_similarity(vectors, vectors) + 1) / 2
    print(sim)
    print(np.sum(sim))


def checkRelation(model: KeyedVectors, tokenMap: Dict, words: List[Tuple[str, str]]):
    vectors = []

    for wordA, wordB in words:
        wordIdA = str(tokenMap[wordA])
        wordIdB = str(tokenMap[wordB])
        try:
            difVector = model[wordIdA] - model[wordIdB]
        except KeyError:
            logging.error(f"At least one key not found ({wordA}, {wordB})")
        else:
            vectors.append(difVector)

    printSimilarity(vectors)


def exampleSimilarity(model, tokenMap):
    def getRandom():
        return str(random.randint(0, len(tokenMap)))

    def getVector():
        while True:
            num = getRandom()
            try:
                return model[num]
            except KeyError:
                pass

    vectors = []
    for _ in range(5):
        a = getVector()
        b = getVector()
        vectors.append(a - b)

    printSimilarity(vectors)


def printMostSimilar(model, tokenMap, positive=(), negative=()):
    if isinstance(positive, str):
        positive = (positive,)
    if isinstance(negative, str):
        negative = (negative,)

    sim = model.most_similar(
        positive=[str(tokenMap[t]) for t in positive],
        negative=[str(tokenMap[t]) for t in negative],
        topn=20,
    )

    rev = {str(v): k for k, v in tokenMap.items()}
    newSim = [(rev[k], v) for k, v in sim]
    pprint(newSim)


def main():
    model = getModel()
    tokenMap = loadDict().token2id
    checkRelation(model, tokenMap, [
        ("król", "królowa"),
        ("mężczyzna", "kobieta"),
    ])
    checkRelation(model, tokenMap, [
        ('atakować', 'atakował'),
        ('zrobić', 'zrobił'),
        ('kupić', 'kupił'),
        ('malować', 'namalował'),
        ('tworzyć', 'stworzył'),
    ])
    exampleSimilarity(model, tokenMap)
    printMostSimilar(
        model, tokenMap, positive=('król', 'kobieta'), negative='mężczyzna')


if __name__ == '__main__':
    """
    https://dumps.wikimedia.org/plwiki/
    https://dumps.wikimedia.org/plwiki/20190601/plwiki-20190601-pages-articles-multistream.xml.bz2
    """
    main()
