import numpy as np
from sklearn.cluster import dbscan

from lab3.stop_list import StopList


class BaseClassification:

    def __init__(self, stopList: StopList, dataToClassify: list = None):
        self.stopList = stopList
        self.dataToClassify = dataToClassify or []

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

    def dbscan(self, eps=5, min_samples=2, **kwargs):
        maxData = len(self.dataToClassify)
        indexes = np.arange(maxData).reshape(-1, 1)
        core, labels = dbscan(indexes, metric=self.metric, eps=eps, min_samples=min_samples,
                              algorithm='brute', n_jobs=-1, **kwargs)
        labels = [lab if lab != -1 else maxData + i for i, lab in enumerate(labels)]
        return labels
