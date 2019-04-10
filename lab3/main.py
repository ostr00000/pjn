import json
import logging
import os
import pickle
from pprint import pprint

from lab3.classification.baseClassification import BaseClassification
from lab3.classification.cache import CacheManager
from lab3.classification.cosine import CosineClassification
from lab3.classification.lcs import LongestCommonSubstring
from lab3.classification.levenshtein import LevenshteinClassification
from lab3.index.davides_bouldin_modified import indexBD
from lab3.index.dunn import indexDunn
from lab3.stop_list import StopList

path = os.path.join('data', 'lines.txt')

os.makedirs('out', exist_ok=True)


def showResult(name: str, cl: BaseClassification):
    jsonFileName = os.path.join('out', name + '.json')
    pickleFileName = os.path.join('out', name + '.pickle')
    distanceMatrixName = os.path.join('out', name[:3] + '_dm.pickle')

    if os.path.exists(pickleFileName):
        with open(pickleFileName, 'rb') as file:
            loadedCl = pickle.load(file)

    else:
        if os.path.exists(distanceMatrixName):
            with open(distanceMatrixName, 'rb') as file:
                loadedCl = pickle.load(file)
                loadedCl.epsilon = cl.epsilon

        else:
            cl.computeDistanceMatrix()
            with open(distanceMatrixName, 'wb') as file:
                pickle.dump(cl, file)
                loadedCl = cl

        loadedCl.dbscan()
        loadedCl.index['davides_bouldin'] = indexBD(loadedCl)
        loadedCl.index['dunn'] = indexDunn(loadedCl)

        with open(pickleFileName, 'wb') as file:
            pickle.dump(loadedCl, file)

        with open(jsonFileName, 'w') as file:
            json.dump(loadedCl.classifiedData, file, ensure_ascii=False, sort_keys=True, indent=4)

    print()
    print(name)
    print(f"Index Davies-Bouldin: {loadedCl.index['davides_bouldin']:.5} (lepiej mniej)")
    print(f"Index Dunn: {loadedCl.index['dunn']:.5} (lepiej więcej)")


def main():
    stopList = StopList()
    stopList.read(path)
    stopList.excludeByWordsMargin(120)
    pprint(stopList.excluded)

    base = BaseClassification(stopList)
    base.load(path)
    base.dataToClassify = sorted(base.dataToClassify)
    pprint(base.dataToClassify)

    CacheManager.prepareCache(base.dataToClassify)

    showResult('cos0.1', CosineClassification(stopList, base.dataToClassify, epsilon=0.1))
    showResult('cos0.2', CosineClassification(stopList, base.dataToClassify, epsilon=0.2))
    showResult('cos0.3', CosineClassification(stopList, base.dataToClassify, epsilon=0.3))

    showResult('lev3', LevenshteinClassification(stopList, base.dataToClassify, epsilon=3))
    showResult('lev5', LevenshteinClassification(stopList, base.dataToClassify, epsilon=5))
    showResult('lev8', LevenshteinClassification(stopList, base.dataToClassify, epsilon=8))
    showResult('lev10', LevenshteinClassification(stopList, base.dataToClassify, epsilon=10))

    showResult('lcs0.3', LongestCommonSubstring(stopList, base.dataToClassify, epsilon=0.3))
    showResult('lcs0.1', LongestCommonSubstring(stopList, base.dataToClassify, epsilon=0.1))
    showResult('lcs0.05', LongestCommonSubstring(stopList, base.dataToClassify, epsilon=0.05))



if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
