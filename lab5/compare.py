from typing import Union

import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity

from accessFunctions import getAllModels, getLoaderPrimaryForm
from classification import Classification
from loader import Loader
from util import LogIter


def getSimilarityVector(baseIndex, vectors: Union[coo_matrix, np.ndarray]):
    if isinstance(vectors, coo_matrix):
        vectors = vectors.tocsr()

    baseVector = vectors[baseIndex]
    out = cosine_similarity(vectors, baseVector)
    out = out[:, 0]
    return out


def getBestNIndexes(vector: np.ndarray, bestN: int):
    ind = np.argpartition(vector, -bestN)[-bestN:]
    sortedBestN = ind[np.argsort(vector[ind])]
    return sortedBestN


def printSimilarText(baseIndex: int, vectors: Union[coo_matrix, np.ndarray], loader: Loader):
    simVec = getSimilarityVector(baseIndex, vectors)
    simInd = getBestNIndexes(simVec, 10)

    for index in simInd:
        print(f"index:{index+1:5}[prob={simVec[index]:5.4}]:\t{' '.join(loader.data[index])}")


noteTestId = 1777
firstNResults = 10
noteResultIds = {
    1777: [1399, 1776, 1777, 6893, 1678, 1677, 1483, 6214, 40129],

}


def printResultFromAllModels():
    noteIndexes = set()
    for model in LogIter(getAllModels(), printStep=1):
        simVec = getSimilarityVector(noteTestId, model.vectors)
        simInd = set(getBestNIndexes(simVec, firstNResults))
        noteIndexes |= simInd

    loader = getLoaderPrimaryForm()
    for index in noteIndexes:
        print(f"programIndex:{index:5} [#{index+1:06}]:\t{' '.join(loader.data[index])}")


def scoreModels():
    approvedIndexes = noteResultIds[noteTestId]
    for model in getAllModels():
        simVec = getSimilarityVector(noteTestId, model.vectors)
        simInd = getBestNIndexes(simVec, firstNResults)

        classified = [ind in approvedIndexes for ind in simInd]
        cl = Classification([True] * len(simInd), classified)
        print(f"{model} precission:{cl.getPrecision()}, recall:{cl.getRecall()}, F1:{cl.getF1()}")
