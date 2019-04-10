import json
import logging
import os
from pprint import pprint

from lab3.classification.baseClassification import BaseClassification
from lab3.classification.cache import CacheManager
from lab3.classification.cosine import CosineClassification
from lab3.classification.lcs import LongestCommonSubstring
from lab3.classification.levenshtein import LevenshteinClassification
from lab3.stop_list import StopList

path = os.path.join('data', 'lines.txt')


def getResult(name: str, classification: BaseClassification, **kwargs):
    if not name.endswith('.json'):
        name += '.json'

    if os.path.exists(name):
        with open(name, 'r') as file:
            return json.load(file)

    data = classification.dbscan(**kwargs)  # TODO
    with open(name, 'w') as file:
        json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=4)
        return data


def main():
    stopList = StopList()
    stopList.read(path)
    stopList.excludeByWordsMargin(100)

    base = BaseClassification(stopList)
    base.load(path)
    base.dataToClassify = sorted(base.dataToClassify)
    pprint(base.dataToClassify)  # TODO

    CacheManager.prepareCache(base.dataToClassify)

    r = getResult('cos', CosineClassification(stopList, base.dataToClassify))
    r = getResult('lcs', LongestCommonSubstring(stopList, base.dataToClassify))
    r = getResult('lev', LevenshteinClassification(stopList, base.dataToClassify))


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
