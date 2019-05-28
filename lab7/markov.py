import numpy as np
import os
from collections import OrderedDict
from functools import partial
from operator import itemgetter
import pprint
from typing import List, Dict, Tuple

from author import Author
from author_loader import loadAuthors
from cache import LocalCache


def authorScore(possibilities: List[Author], testBookName: str) -> Dict[str, float]:
    with open(os.path.join('data', testBookName)) as book:
        sentences = []
        for sentence in list(Author.sentenceGen(book))[:100]:
            words = ' '.join(filter(None, Author.SPLIT_PATTERN.split(sentence)))
            if words:
                sentences.append(words)

    results = {}
    for i, pos in enumerate(possibilities):
        try:
            print(f"[{i}] = {pos.name}")
        except UnicodeEncodeError:
            pass

        totalProb = 0
        for sentence in sentences:
            prob = pos.sentenceProb(sentence)
            totalProb += prob
        results[pos.name] = totalProb
    return results


def findBest(testBooks: Tuple, testBook: str):
    authors = loadAuthors(testBooks)
    score = authorScore(list(authors.values()), testBook)
    score = sorted(score.items(), key=itemgetter(1))
    return score


def main():
    testBooks = {
        'Agata_Christie': 'Tajemnica_Wawrzynow.txt',
        'Janusz_A_Zajdel': 'Awaria.txt',
        'Paulo_Coelho': 'Alchemik.txt',
        'George_Orwell': 'Orwell_George_-_Rok_1984.txt',
        'Sapkowski_Andrzej': 'Pani_Jeziora.txt',
        'Andre_Norton': 'Andre_Norton_-_Prekursorka.txt',
        'Dick_Philip_K': 'Dick_Philip_K_-_Kolonia.txt',
        'Gordon_R_Dickson': 'Gordon_R_Dickson_-_Nekromanta.txt',
        'Lem_Stanislaw': 'Lem_Stanislaw_-_Bajki_robotow.txt',
        'Terry_Pratchett': 'Terry_Pratchett_-_Ruchome_Obrazki.txt',
    }
    firstN = 10
    scores = []
    for name, testBook in testBooks.items():
        pFindBest = partial(findBest, tuple(testBooks.values()), testBook)
        result = LocalCache.load(f'{name}.scoreResult', pFindBest)
        score = list(OrderedDict(result).keys()).index(name)
        scores.append(score)

        print(f"Author: {name} has score: {score} for book: {testBook}")
        print(f"First {firstN} best results: \n{pprint.pformat(result[:firstN])}\n\n")
    else:
        print(f"scores: {scores}")
        print(f"Average score: {sum(scores)/len(testBooks)}, std: {np.std(scores)}")


if __name__ == '__main__':
    main()
