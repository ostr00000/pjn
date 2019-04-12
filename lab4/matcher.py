from functools import partial
from queue import PriorityQueue
from typing import Dict, Callable, List

from metric import levMetric

THRESHOLD = 1e-7
LEN_PARAM = 100


def nBestWords(nBest: int, errorWord: str, fun: Callable[[str, str], float],
               possibleWords: Dict[str, float]) -> List[str]:
    pq = PriorityQueue()
    queueLimit = nBest

    for correctWord, freq in possibleWords.items():
        prob = fun(errorWord, correctWord) / \
               max(1, LEN_PARAM * abs(len(errorWord) - len(correctWord)))

        val = prob * freq
        if queueLimit:
            queueLimit -= 1
        else:
            pq.get()

        pq.put((val, correctWord))

    probAndWords = reversed([pq.get() for _ in range(nBest)])
    words = [word for prob, word in probAndWords if prob > 1e-7]
    return words


best3Words = partial(nBestWords, 3)


def bestCorrectWord(errorWord: str, fun: Callable[[str, str], float],
                    possibleWords: Dict[str, float]) -> float:
    best = 0., None
    for correctWord, freq in possibleWords.items():
        prob = fun(errorWord, correctWord) / \
               max(1, LEN_PARAM * abs(len(errorWord) - len(correctWord)))

        val = prob * freq
        if val > best[0]:
            best = val, correctWord

    return best[1]


def levErrorProbability(xStr: str, yStr: str):
    return 1 - (levMetric(xStr, yStr) / max(len(xStr), len(yStr)))
