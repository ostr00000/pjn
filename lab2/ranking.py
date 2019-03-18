from typing import Tuple, List


class Ranking:

    def __init__(self, ranking: List[Tuple[str, int]]):
        self.ranking = ranking

    def countHapaxLegomena(self) -> int:
        return sum(1 for _key, value in self.ranking if value == 1)

    def getWordsCover(self, percent=50) -> int:
        total = sum(value for _key, value in self.ranking)
        half = total * percent / 100

        coverage = 0
        wordsCounter = 0

        for _key, value in self.ranking:
            coverage += value
            wordsCounter += 1
            if coverage >= half:
                break

        return wordsCounter

    def __len__(self):
        return len(self.ranking)

    def __iter__(self):
        return iter(self.ranking)
