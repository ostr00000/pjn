import os
import pickle

from util import entryExitDec


class LocalCache:
    THREADS = 8

    @classmethod
    @entryExitDec
    def load(cls, name, orFunction=lambda: None):
        path = os.path.join('.cache', name)
        if os.path.exists(path):
            with open(path, 'rb') as file:
                obj = pickle.load(file)
                return obj

        obj = orFunction()
        LocalCache.save(obj, path)
        return obj

    @staticmethod
    def save(obj, path):
        dirName = os.path.dirname(path)
        os.makedirs(dirName, exist_ok=True)
        with open(path, 'wb') as file:
            pickle.dump(obj, file)
