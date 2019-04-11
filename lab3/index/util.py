from functools import lru_cache
from itertools import combinations
from typing import Dict, List

import numpy as np


from lab3.classification.baseClassification import BaseClassification

cluster_t = Dict[int, List[str]]


@lru_cache(1)
def getDistanceBetweenClusters(cl: BaseClassification):
    clustersNumber = len(cl.classifiedData)
    distanceBetweenClusters = np.zeros((clustersNumber, clustersNumber))
    for (cIndex1, c1), (cIndex2, c2) in combinations(enumerate(cl.classifiedData.values()), 2):
        totalSum = 0
        for e1 in c1:
            partSum = sum(cl.distanceMatrix[cl.dataToIndex[e1], cl.dataToIndex[e2]] for e2 in c2)
            totalSum += partSum / len(c2)
        avrDistance = totalSum / len(c1)

        distanceBetweenClusters[cIndex1, cIndex2] = avrDistance
        distanceBetweenClusters[cIndex2, cIndex1] = avrDistance

    return distanceBetweenClusters


def getAvrDistInCluster(cl: BaseClassification):
    avrDistInCluster = np.empty(len(cl.classifiedData))
    for i, clusterContent in enumerate(cl.classifiedData.values()):
        totalClusterDistance = 0
        for e1, e2 in combinations(clusterContent, 2):
            totalClusterDistance += cl.distanceMatrix[cl.dataToIndex[e1], cl.dataToIndex[e2]]

        avrDistInCluster[i] = totalClusterDistance
    return avrDistInCluster
