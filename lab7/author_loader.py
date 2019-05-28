import os
from functools import lru_cache
from os import DirEntry
from typing import List, Dict, Tuple

from author import Author
from lab5.cache import LocalCache


def _getSingleAuthor(authorName):
    def createAuthor():
        author = Author(authorName)
        for dirEntry in os.scandir('data'):
            _authorName = dirEntry.name.split('_-_')[0]
            if _authorName == authorName:
                try:
                    with open(dirEntry.path) as file:
                        author.loadBooks(file)
                except UnicodeDecodeError:
                    pass
        author.calcProbability()
        return author

    return LocalCache.load(authorName, createAuthor,
                           path=os.path.join('.cache', 'authors', authorName))


def _getBooks():
    allEntries = list(os.scandir('data'))
    allEntries.sort(key=lambda d: d.stat().st_size)
    yield from allEntries


@lru_cache()
def loadAuthors(libriProhibiti: Tuple[str]) -> Dict[str, Author]:
    authors = {}
    dirElem = len(next(os.walk('data'))[2])
    for i, dirEntry in enumerate(_getBooks()):  # type: int, DirEntry
        try:
            if dirEntry.name in libriProhibiti:
                continue
            print(f'{i}/{dirElem} = {i/dirElem*100:.3}% ({dirEntry})')
        except UnicodeEncodeError:
            continue

        authorName = dirEntry.name.split('_-_')[0]
        if authorName not in authors:
            author = _getSingleAuthor(authorName)
            if author:
                authors[authorName] = author

    return authors
