import numpy as np

from lab3.classification.baseClassification import BaseClassification
from lab3.index.util import getDistanceBetweenClusters


def indexDunn(classification: BaseClassification):
    distanceBetweenClusters = getDistanceBetweenClusters(classification)
    clustersNumber = len(classification.classifiedData)

    for i in range(clustersNumber):
        distanceBetweenClusters[i, i] = np.inf

    minDistanceBetweenClusters = np.min(distanceBetweenClusters)
    maxClusterSize = max(len(c) for c in classification.classifiedData.values())

    return minDistanceBetweenClusters / maxClusterSize
