import itertools
from typing import Dict, List

import numpy as np

cluster_t = Dict[str, List[str]]


def getDistanceBetweenClusters(cluster: cluster_t, dataToIndex: Dict[str, int],
                               elementDistance: np.ndarray):
    clustersNumber = len(cluster)
    distanceBetweenClusters = np.zeros((clustersNumber, clustersNumber))
    for (cIndex1, c1), (cIndex2, c2) in itertools.combinations(enumerate(cluster.values()), 2):
        minDistance = min(elementDistance[dataToIndex[e1], dataToIndex[e2]]
                          for e1 in c1 for e2 in c2)
        distanceBetweenClusters[cIndex1, cIndex2] = minDistance
        distanceBetweenClusters[cIndex2, cIndex1] = minDistance

    return distanceBetweenClusters


def getAvrDistInCluster(cluster: cluster_t, dataToIndex: Dict[str, int],
                        elementDistance: np.ndarray):
    avrDistInCluster = np.empty(len(cluster))
    for i, clusterContent in enumerate(cluster.values()):
        totalClusterDistance = 0
        for e1, e2 in itertools.combinations(clusterContent, 2):
            totalClusterDistance += elementDistance[dataToIndex[e1], dataToIndex[e2]]

        avrDistInCluster[i] = totalClusterDistance
    return avrDistInCluster


def indexBD(rawData: List[str], cluster: cluster_t, elementDistance: np.ndarray):
    dataToIndex = {data: i for i, data in enumerate(rawData)}
    avrDistInCluster = getAvrDistInCluster(cluster, dataToIndex, elementDistance)
    distanceBetweenClusters = getDistanceBetweenClusters(cluster, dataToIndex, elementDistance)

    indexSum = 0
    for cIndex1, c1 in enumerate(cluster.values()):
        maxPartIndex = 0
        for cIndex2, c2 in enumerate(cluster.values()):
            if cIndex1 == cIndex2:
                continue

            nom = avrDistInCluster[cIndex1] + avrDistInCluster[cIndex2]
            den = distanceBetweenClusters[cIndex1, cIndex2]
            partIndex = nom / den
            maxPartIndex = max(partIndex, maxPartIndex)

        indexSum += maxPartIndex

    index = indexSum / len(cluster)
    return index


def main():
    dataRaw = ['a', 'b', 'c', 'eee', 'fff', 'gg']
    clusters = {'1': ['a', 'b', 'c'], '2': ['eee', 'fff'], '10': ['gg']}
    distMat = np.array([[0 if d == e else
                         1 if len(d) == len(e) else
                         max(len(d), len(e)) - min(len(d), len(e)) + 1
                         for d in dataRaw] for e in dataRaw])
    for i, d in enumerate(dataRaw):
        print(f'{d:3} = {distMat[i]}')
    index = indexBD(dataRaw, clusters, distMat)
    print(index)


if __name__ == '__main__':
    main()
