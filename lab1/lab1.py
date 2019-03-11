import pickle
from pprint import pprint

from language import LanguageManager
from metrics import Euclidean, Manhattan, Maximum, Cosine

manSaveName = 'normalized.save'


def main():
    try:
        with open(manSaveName, 'rb') as f:
            manager = pickle.load(f)
    except FileNotFoundError:
        manager = LanguageManager()
        manager.process()
        manager.normalize()
        with open(manSaveName, 'wb') as f:
            pickle.dump(manager, f)

    try:
        while True:
            text = input("get text to recognise language\n")
            for metric in (Euclidean, Manhattan, Maximum, Cosine):
                statistics = manager.guessLanguage(text, metric)
                print(f"Metric: {metric.__name__}")
                pprint(statistics)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
