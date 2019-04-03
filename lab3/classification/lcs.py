import logging
from difflib import SequenceMatcher

from lab3.classification.baseClassification import BaseClassification

logger = logging.getLogger(__name__)


class LongestCommonSubstring(BaseClassification):

    def metric(self, x, y):
        xStr = self.dataToClassify[int(x)]
        yStr = self.dataToClassify[int(y)]
        if int(x) % 100 == 0 and int(y) % 100 == 0:
            logger.warning(f"x={int(x)},y={int(y)}")

        sm = SequenceMatcher(None, xStr, yStr)
        lm = sm.find_longest_match(0, len(xStr), 0, len(yStr))
        den = max(len(xStr), len(yStr))
        return 1 - (lm.size / den)
