from typing import Union

import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity

from loader import Loader


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
        print(f"index:{index+1:5}[prob={simVec[index]:6.4}]:\t{' '.join(loader.data[index])}")
