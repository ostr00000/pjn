import json
import os
from collections import defaultdict
from pprint import pprint

from lab3.classification.baseClassification import BaseClassification
from lab3.classification.cache import CacheManager
from lab3.classification.cosine import CosineClassification
from lab3.classification.lcs import LongestCommonSubstring
from lab3.classification.levenshtein import LevenshteinClassification
from lab3.stop_list import StopList

import logging


path = os.path.join('data', 'lines.txt')


def groupScan(scan, data):
    result = defaultdict(list)
    for i, group in enumerate(scan):
        result[str(group)].append(data[i])
    return dict(result)


def getResult(name, fun):
    if not name.endswith('.json'):
        name += '.json'

    if os.path.exists(name):
        with open(name, 'r') as file:
            return json.load(file)

    data = fun()
    with open(name, 'w') as file:
        json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=4)
        return data


def main():
    sl = StopList()
    sl.read(path)
    sl.excludeByWordsMargin(100)

    c = BaseClassification(sl)
    c.load(path)
    c.dataToClassify = sorted(c.dataToClassify)
    pprint(c.dataToClassify)
    CacheManager.prepareCache(c.dataToClassify)

    # def cos():
    #     ll = CosineClassification(sl, c.dataToClassify)
    #     scan = ll.dbscan(eps=0.15, min_samples=2)
    #     res = groupScan(scan, c.dataToClassify)
    #     return res
    #
    # result = getResult('cos', cos)
    # pprint(result)

    def lcs():
        ll = LongestCommonSubstring(sl, c.dataToClassify)
        scan = ll.dbscan(eps=0.5, min_samples=2)
        res = groupScan(scan, c.dataToClassify)
        return res

    result = getResult('lcs', lcs)
    pprint(result)

    # def lev():
    #     ll = LevenshteinClassification(sl, c.dataToClassify)
    #     scan = ll.dbscan(eps=5, min_samples=2, n_jobs=-1)
    #     res = groupScan(scan, c.dataToClassify)
    #     return res
    #
    # result = getResult('lev', lev)
    # pprint(result)


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
