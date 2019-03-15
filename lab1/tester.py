from collections import defaultdict
from operator import itemgetter
from typing import Dict, Any

from classification import Classification
from language import LanguageManager
from metrics import Cosine

manSaveName = 'normalized.save'


def flipDict(data: Dict[Any, Dict]) -> Dict[Any, Dict]:
    retDict = defaultdict(dict)

    for key1, firstLevel in data.items():
        for key2, val in firstLevel.items():
            retDict[key2][key1] = val

    return retDict


def flipDict3(data: Dict[Any, Dict[Any, Dict]]) -> Dict[Any, Dict[Any, Dict]]:
    for key, subDict in data.items():
        data[key] = flipDict(subDict)
    return flipDict(data)


def measure(filename, searchLang='polish', metric=Cosine):
    manager = LanguageManager.getManager()
    nGram2List = defaultdict(list)
    baseList = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.lstrip()
            if not line:
                continue
            baseLang, text = line.split(' ', 1)
            baseList.append(baseLang == searchLang)

            guess = manager.guessLanguage(text)
            guess = flipDict(guess[0][metric])

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


def main():
    # for lang in ("english", "german", "polish", "spanish", "italian"):
    for lang in ("english", "polish"):
        print(f"\nLanguage: {lang}")
        measure("myfile.txt", lang)


if __name__ == '__main__':
    main()
