import logging

from scipy.spatial.distance import cosine

from lab3.classification.baseClassification import BaseClassification
from lab3.classification.cache import CacheManager

logger = logging.getLogger(__name__)


class CosineClassification(BaseClassification):

    def metric(self, x, y, **kwargs):
        a = self.dataToClassify[int(x)]
        b = self.dataToClassify[int(y)]
        xN = CacheManager.getNGram(a)
        yN = CacheManager.getNGram(b)
        if int(x) % 100 == 0 and int(y) % 100 == 0:
            logger.warning(f"x={int(x)},y={int(y)}")

        dist = cosine(xN.vector, yN.vector)
        return dist
