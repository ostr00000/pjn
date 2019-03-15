import numpy as np


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
        """vectors a, b are normalized, ||a|| = ||b|| = 1"""
        # lengthA: float = np.sqrt(np.sum(a ** 2))
        # lengthB: float = np.sqrt(np.sum(b ** 2))
        # div = lengthA * lengthB
        # if div == 0:
        #     return 1.
        acc: float = np.sum(a * b)
        return 1. - acc


ALL_METRIC = (Euclidean, Manhattan, Maximum, Cosine)
