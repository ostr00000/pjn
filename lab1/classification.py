from typing import List


class Classification:

    def __init__(self, baseData: List, classifiedData: List):
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.tn = 0

        for b, c in zip(baseData, classifiedData):
            if bool(b):
                if bool(c):
                    self.tp += 1
                else:
                    self.fn += 1
            else:
                if bool(c):
                    self.fp += 1
                else:
                    self.tn += 1

    def getPrecision(self):
        d = (self.tp + self.fp)
        if d == 0:
            return 0
        return self.tp / d

    def getRecall(self):
        d = (self.tp + self.fn)
        if d == 0:
            return 0
        return self.tp / d

    def getF1(self):
        p = self.getPrecision()
        r = self.getRecall()
        d = p + r
        if d == 0:
            return 0
        return 2 * p * r / d

    def getAccuracy(self):
        d = (self.tp + self.fp + self.fn + self.tn)
        if d == 0:
            return 0
        return (self.tp + self.tn) / d
