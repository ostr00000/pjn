import os

from cache import LocalCache
from compare import printSimilarText
from graph import GraphModel
from loader import Loader
from primary_form import PrimaryForm

primaryFormPath = os.path.join('data', 'odm.txt')


def getPrimaryForm() -> PrimaryForm:
    return LocalCache.load('primaryForm', lambda: PrimaryForm(primaryFormPath))


def getLoaderPrimaryForm() -> Loader:
    return LocalCache.load('loaderPrimaryForm', lambda: Loader(primaryForm=getPrimaryForm()))


def getGraph() -> GraphModel:
    def _getGraph():
        from graph import GraphModel
        loader = getLoaderPrimaryForm()
        g = GraphModel(loader)
        g.processGraphs(slice(51555))
        return g

    return LocalCache.load('graph', _getGraph)


def main():
    graph = getGraph()
    loader = getLoaderPrimaryForm()

    printSimilarText(0, graph.graphs, loader)


if __name__ == '__main__':
    main()
