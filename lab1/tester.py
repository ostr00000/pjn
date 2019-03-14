import pickle
from collections import defaultdict
from operator import itemgetter

from typing import Dict, Any

from classification import Classification
from language import LanguageManager
from metrics import Cosine

manSaveName = 'normalized.save'


def getManager() -> LanguageManager:
    try:
        with open(manSaveName, 'rb') as f:
            manager = pickle.load(f)
    except FileNotFoundError:
        manager = LanguageManager()
        manager.process()
        manager.normalize()
        with open(manSaveName, 'wb') as f:
            pickle.dump(manager, f)
    return manager


def flipDict(data: Dict[Any, Dict]) -> Dict[Any, Dict]:
    retDict = defaultdict(dict)

    for key1, firstLevel in data.items():
        for key2, val in firstLevel.items():
            retDict[key2][key1] = val

    return retDict


def measure(filename, searchLang='polish'):
    manager = getManager()
    nGram2List = defaultdict(list)
    baseList = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.lstrip()
            if not line:
                continue
            baseLang, text = line.split(' ', 1)
            baseList.append(baseLang == searchLang)

            guess = manager.guessLanguage(text, Cosine)
            guess = flipDict(guess)

            for nGram, lang in guess.items():
                bestLang = min(lang.items(), key=itemgetter(1))[0]
                nGram2List[nGram].append(bestLang == searchLang)

        for nGram, data in nGram2List.items():
            print(f"{nGram}-Gram")
            c = Classification(baseList, data)
            print(f"Precision: {c.getPrecision()}")
            print(f"Recall: {c.getRecall()}")
            print(f"F1: {c.getF1()}")
            print(f"Accuracy: {c.getAccuracy()}\n")


if __name__ == '__main__':
    for lang in ("english", "german", "polish", "spanish", "italian"):
        print(f"\nLanguage: {lang}")
        measure("myfile.txt", lang)
