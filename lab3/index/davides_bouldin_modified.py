from typing import Dict, List

import numpy as np

from lab3.classification.baseClassification import BaseClassification
from lab3.index.util import getAvrDistInCluster, getDistanceBetweenClusters

cluster_t = Dict[int, List[str]]


def indexBD(classification: BaseClassification):
    avrDistInCluster = getAvrDistInCluster(classification)
    distanceBetweenClusters = getDistanceBetweenClusters(classification)

    indexSum = 0
    for cIndex1, c1 in enumerate(classification.classifiedData.values()):
        maxPartIndex = 0
        for cIndex2, c2 in enumerate(classification.classifiedData.values()):
            if cIndex1 == cIndex2:
                continue

            nom = avrDistInCluster[cIndex1] + avrDistInCluster[cIndex2]
            den = distanceBetweenClusters[cIndex1, cIndex2]
            partIndex = nom / den
            maxPartIndex = max(partIndex, maxPartIndex)

        indexSum += maxPartIndex

    index = indexSum / len(classification.classifiedData)
    return index


def main():
    dataRaw = ['a', 'b', 'c', 'eee', 'fff', 'gg']
    clusters = {0: ['a', 'b', 'c'], 1: ['eee', 'fff'], 2: ['gg']}
    distMat = np.array([[0 if d == e else
                         1 if len(d) == len(e) else
                         max(len(d), len(e)) - min(len(d), len(e)) + 1
                         for d in dataRaw] for e in dataRaw])
    for i, d in enumerate(dataRaw):
        print(f'{d:3} = {distMat[i]}')
    c = BaseClassification(dataToClassify=dataRaw)
    c.classifiedData = clusters
    c.distanceMatrix = distMat

    index = indexBD(c)
    print(index)


if __name__ == '__main__':
    main()
