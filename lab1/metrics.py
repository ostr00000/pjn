from math import sqrt


class Metric:
    def __init__(self):
        self.acc = 0

    def addPair(self, a, b):
        raise NotImplementedError

    def getResult(self):
        return self.acc


class Euclidean(Metric):

    def addPair(self, a, b):
        self.acc += (a - b) ** 2


class Manhattan(Metric):
    def addPair(self, a, b):
        self.acc += abs(a - b)


class Maximum(Metric):
    def addPair(self, a, b):
        self.acc = max(self.acc, abs(a - b))


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
