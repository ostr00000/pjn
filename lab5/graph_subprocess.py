import sys

from lab5.cache import LocalCache
from lab5.graph import GraphModel
from lab5.loader import Loader
from lab5.util import timeDec


@timeDec
def main():
    graphName = sys.argv[1]
    print(graphName)
    graphData: str = graphName.split('.')[0]
    baseName = graphData.split('_')
    degree = int(baseName[0][-1])

    baseSlice = baseName[1].split(':')
    graphSlice = slice(int(baseSlice[0]), int(baseSlice[1]))

    def calcGraph():
        loader: Loader = LocalCache.load('loaderPrimaryForm')
        gm = GraphModel(loader, degree)
        gm.processGraphs(graphSlice)
        return gm

    LocalCache.load(graphName, calcGraph)


if __name__ == '__main__':
    main()
