import json
import logging
import os
from functools import lru_cache
from itertools import product
from typing import List, Iterable

from lab1.ngram import NGram

logger = logging.getLogger(__name__)

filename = 'possibleKeys.txt'


def loadPossibleKeys():
    if not os.path.exists(filename):
        return None

    with open(filename, 'r') as file:
        return json.load(file)


class CacheManager:
    _possibleKeys = loadPossibleKeys()
    counter = 0
    N_GRAM_SIZE = 2

    @classmethod
    def prepareCache(cls, dataToClassify: List[str]):
        if os.path.exists(filename):
            return

        logger.info("creating possible chars")
        possibleKeys = set(char for data in dataToClassify for char in data)
        cls._possibleKeys = [''.join(keys) for keys in product(possibleKeys, repeat=cls.N_GRAM_SIZE)]
        cls._savePossibleKeys(cls._possibleKeys)
        logger.info("Chars created successfully")

    @staticmethod
    def _savePossibleKeys(possibleKeys: Iterable[str]):
        with open(filename, 'w') as file:
            json.dump(possibleKeys, file)

    @classmethod
    @lru_cache(None)
    def getNGram(cls, data: str):
        # logger.warning(f"create nGram:{cls.counter}")
        # cls.counter += 1

        nGram = NGram(cls.N_GRAM_SIZE, processText=True)
        nGram.process(data)
        nGram.normalize()
        nGram.prepareCache(possibleKeys=cls._possibleKeys)
        return nGram
