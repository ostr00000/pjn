from pprint import pprint

from language import LanguageManager

manSaveName = 'normalized.save'


def main():
    manager = LanguageManager.getManager(manSaveName)

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
