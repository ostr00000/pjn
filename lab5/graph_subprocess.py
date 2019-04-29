import sys
import os
from lab5.graph import GraphModel
from lab5.cache import LocalCache


def main():
    graphName: str = sys.argv[0].split('.')[0]
    baseName = graphName.split('_')
    degree = int(baseName[0][-1])

    baseSlice = baseName[1].split(':')
    graphSlice = slice(int(baseSlice[0]), int(baseSlice[1]))

    def calcGraph():
        loader = LocalCache.load('loader')
        gm = GraphModel(loader, degree)
        gm.processGraphs(graphSlice)
        return gm

    LocalCache.load(graphName, calcGraph)


if __name__ == '__main__':
    main()
