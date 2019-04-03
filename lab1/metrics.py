import numpy as np
from scipy.spatial.distance import cosine


class Metric:

    def getDistance(self, a: np.ndarray, b: np.ndarray) -> float:
        raise NotImplementedError


class Euclidean(Metric):

    def getDistance(self, a: np.ndarray, b: np.ndarray) -> float:
        """a<-[-1,1], b<-[-1,1], (a-b)**2<-[0, 4]"""
        acc = (a - b) ** 2
        return np.sqrt(np.sum(acc)) / (2 * np.sqrt(acc.size))


class Manhattan(Metric):
    def getDistance(self, a: np.ndarray, b: np.ndarray) -> float:
        """a<-[-1,1], b<-[-1,1], |a-b|<-[0, 2]"""
        acc: np.ndarray = np.abs(a - b)
        return np.sum(acc) / (2 * acc.size)


class Maximum(Metric):
    def getDistance(self, a: np.ndarray, b: np.ndarray) -> float:
        """a<-[-1,1], b<-[-1,1], |a-b|<-[0, 2]"""
        return np.max(np.abs(a - b)) / 2


class Cosine(Metric):
    def getDistance(self, a: np.ndarray, b: np.ndarray) -> float:
        return cosine(a, b)


ALL_METRIC = (Euclidean, Manhattan, Maximum, Cosine)
