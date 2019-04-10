from collections import defaultdict

import numpy as np
from sklearn.cluster import dbscan
from sklearn.neighbors import NearestNeighbors

from lab3.stop_list import StopList


class BaseClassification:

    def __init__(self, stopList: StopList, dataToClassify: list = None):
        self.stopList = stopList
        self.dataToClassify = dataToClassify or []
        self.classifiedData = defaultdict(list)
        self.distanceMatrix = None

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

    def dbscan(self, eps=5, min_samples=2):
        maxData = len(self.dataToClassify)
        indexes = np.arange(maxData).reshape(-1, 1)

        neighbors_model = NearestNeighbors(radius=eps, metric=self.metric, n_jobs=-1)
        neighbors_model.fit(indexes)
        self.distanceMatrix, neighborhoods = neighbors_model.radius_neighbors(indexes, eps)

        core, labels = dbscan(self.distanceMatrix, metric='precomputed', min_samples=min_samples)
        self.setLabels(labels)

    def setLabels(self, labels: np.ndarray):
        lastClusterIndex = np.max(labels)
        for label, line in zip(labels, self.dataToClassify):
            label = int(label)
            if label == -1:
                label = lastClusterIndex
                lastClusterIndex += 1

            self.classifiedData[label].append(line)
