import os
import pickle

from graph import GraphModel
from util import SubprocessSplitter


class LocalCache:
    @classmethod
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
    def loadGraph(name, size=100):
        gr = LocalCache.load(name)
        if gr:
            return gr

        grList = LocalCache._createGraph(name, size)

        gm = GraphModel(None, grList[0].degree)
        gm.graphs.extend(gr.graphs for gr in grList)
        LocalCache.save(gm, os.path.join('.cache', name))

    @staticmethod
    def _createGraph(baseName, size):
        with SubprocessSplitter() as ss:
            chunkSize = size // 8
            names = []
            for part in range(8):
                n = f'{baseName}_{part*chunkSize}:{(part+1)*chunkSize}.part'
                names.append(n)
                ss.run(n)

        return [LocalCache.load(name) for name in names]

    @staticmethod
    def save(obj, path):
        dirName = os.path.dirname(path)
        os.makedirs(dirName, exist_ok=True)
        with open(path, 'wb') as file:
            pickle.dump(obj, file)
