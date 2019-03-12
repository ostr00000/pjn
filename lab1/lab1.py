import pickle
from pprint import pprint

from language import LanguageManager

manSaveName = 'normalized.save'


def getManager():
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


def main():
    manager = getManager()

    try:
        while True:
            text = input("Get text to recognise language\n")
            if not text:
                continue
            statistics = manager.guessLanguage(text)
            pprint(statistics)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
