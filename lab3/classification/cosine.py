import logging

from decorator import decorator

from lab1.metrics import Cosine
from lab3.classification.baseClassification import BaseClassification
from lab3.classification.cache import CacheManager

logger = logging.getLogger(__name__)


@decorator
def printer(fun, *args, **kwargs):
    self, x, y, *_ = args
    logger.warning(f"x={int(x)},y={int(y)}")
    return fun(*args, **kwargs)


class CosineClassification(BaseClassification):
    _metric = Cosine()

    # @printer
    def metric(self, x, y, **kwargs):
        a = self.dataToClassify[int(x)]
        b = self.dataToClassify[int(y)]
        xN = CacheManager.getNGram(a)
        yN = CacheManager.getNGram(b)
        if int(x) % 100 == 0 and int(y) % 100 == 0:
            logger.warning(f"x={int(x)},y={int(y)}")

        dist = self._metric.getDistance(xN.vector, yN.vector)
        return dist
