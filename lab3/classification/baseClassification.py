import time
from collections import defaultdict

import numpy as np
from decorator import decorator
from sklearn.cluster import dbscan
from sklearn.metrics import pairwise_distances

from lab3.stop_list import StopList


@decorator
def timeDec(fun, *args, **kwargs):
    t0 = time.time()
    try:
        return fun(*args, **kwargs)
    finally:
        tx = time.time()
        print(f'total time: {tx - t0}')


class BaseClassification:

    def __init__(self, stopList: StopList = None, dataToClassify: list = None, epsilon: float = 0.5):
        self.stopList = stopList
        self.dataToClassify = dataToClassify or []
        self.classifiedData = defaultdict(list)
        self.distanceMatrix = None
        self.dataToIndex = {v: i for i, v in enumerate(self.dataToClassify)}
        self.epsilon = epsilon
        self.index = {'dunn': None, 'davides_bouldin': None}

    def load(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip().lower()
                nonEmptyWords = filter(None, self.stopList.PATTERN.split(line))
                filteredWords = filter(lambda x: x not in self.stopList.excluded, nonEmptyWords)
                newLine = ' '.join(filteredWords)
                if not newLine:
                    print(f"removing too common name: '{line}'")
                    continue

                self.dataToClassify.append(newLine)

    def metric(self, x, y):
        raise NotImplementedError

    @timeDec
    def computeDistanceMatrix(self):
        indexes = np.arange(len(self.dataToClassify)).reshape(-1, 1)
        self.distanceMatrix = pairwise_distances(indexes, metric=self.metric, n_jobs=-1)

    def dbscan(self):
        core, labels = dbscan(self.distanceMatrix, metric='precomputed',
                              eps=self.epsilon, min_samples=2, n_jobs=-1)

        lastClusterIndex = int(np.max(labels))
        for label, line in zip(labels, self.dataToClassify):
            label = int(label)  # change numpy int64 to int (need to save json)
            if label == -1:
                lastClusterIndex += 1
                label = lastClusterIndex

            self.classifiedData[label].append(line)
