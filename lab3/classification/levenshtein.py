import logging

from leven import levenshtein

from lab3.classification.baseClassification import BaseClassification

logger = logging.getLogger(__name__)


class LevenshteinClassification(BaseClassification):

    def metric(self, x, y):
        if int(x) % 100 == 0 and int(y) % 100 == 0:
            logger.warning(f"x={int(x)},y={int(y)}")

        x = self.dataToClassify[int(x)]
        y = self.dataToClassify[int(y)]
        return levenshtein(x, y)
