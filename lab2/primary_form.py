from collections import defaultdict
from operator import itemgetter
from typing import Iterable

import regex

from ranking import Ranking


class PrimaryForm:
    SPLIT_PATTERN: regex.Regex = regex.compile('\P{L}')

    def __init__(self, filename: str):
        self.dictionary = {}
        primaryForms = set()
        currentLetter = None

        with open(filename, 'r') as file:
            for line in file:
                words = line.rstrip().split(', ')
                if not words:
                    continue
                primaryForm = words[0]

                if currentLetter != primaryForm[0].lower():
                    currentLetter = primaryForm[0].lower()
                    print(currentLetter)

                for word in words:
                    if word in primaryForms:
                        continue
                    self.dictionary[word] = primaryForm
                primaryForms.add(primaryForm)

    def generate(self, filename: str, useSeparators=False) -> Iterable[str]:
        if useSeparators:
            for word in self._generate(filename, useEndLine=True):
                yield word
                if word != '\n':
                    yield ' '
        else:
            yield from self._generate(filename, useEndLine=False)

    def _generate(self, filename: str, useEndLine=False) -> Iterable[str]:
        with open(filename, 'r') as file:
            for number, line in enumerate(file):
                words = filter(None, self.SPLIT_PATTERN.split(line))

                for word in words:
                    try:
                        yield self.dictionary[word]
                    except KeyError:
                        yield word

                if useEndLine:
                    yield '\n'

                if number % 100 == 0:
                    print(f"line: {number}")

    def getRankingForFile(self, filename) -> Ranking:
        repetition = defaultdict(lambda: 0)

        for baseWord in self._generate(filename):
            repetition[baseWord] += 1

        ranking = sorted(repetition.items(), key=itemgetter(1), reverse=True)
        return Ranking(ranking)
