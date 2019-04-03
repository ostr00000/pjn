from leven import levenshtein

from lab3.classification.baseClassification import BaseClassification


class LevenshteinClassification(BaseClassification):

    def metric(self, x, y):
        x = self.dataToClassify[int(x)]
        y = self.dataToClassify[int(y)]
        return levenshtein(x, y)
