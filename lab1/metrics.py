from math import sqrt


class Metric:
    def __init__(self):
        self.acc = 0
        self.n = 0

    def addPair(self, a, b):
        raise NotImplementedError

    def getResult(self):
        return NotImplementedError


class Euclidean(Metric):

    def addPair(self, a, b):
        """a<-[-1,1], b<-[-1,1], (a-b)**2<-[0, 4]"""
        self.acc += ((a - b) / 2) ** 2
        self.n += 1

    def getResult(self):
        """acc<-[0, n]"""
        return sqrt(self.acc / self.n)


class Manhattan(Metric):

    def addPair(self, a, b):
        self.acc += abs(a - b)
        self.n += 1

    def getResult(self):
        """a<-[-1,1], b<-[-1,1], |a-b|<-[0, 2]"""
        return self.acc / (2 * self.n)


class Maximum(Metric):
    def addPair(self, a, b):
        self.acc = max(self.acc, abs(a - b))

    def getResult(self):
        """a<-[-1,1], b<-[-1,1], |a-b|<-[0, 2]"""
        return self.acc / 2


class Cosine(Metric):
    def __init__(self):
        super().__init__()
        self.lengthA = 0
        self.lengthB = 0

    def addPair(self, a, b):
        self.lengthA += a ** 2
        self.lengthB += b ** 2
        self.acc += a * b

    def getResult(self):
        self.lengthA = sqrt(self.lengthA)
        self.lengthB = sqrt(self.lengthB)
        div = (self.lengthA * self.lengthB)
        if not div:
            return 1.
        return 1. - self.acc / div


ALL_METRIC = (Euclidean, Manhattan, Maximum, Cosine)
