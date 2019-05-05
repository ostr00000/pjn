import os
from functools import partial

from cache import LocalCache
from compare import printSimilarText
from graph import GraphModel
from loader import Loader
from primary_form import PrimaryForm
from util import timeDec

primaryFormPath = os.path.join('data', 'odm.txt')


def getPrimaryForm() -> PrimaryForm:
    return LocalCache.load('primaryForm', lambda: PrimaryForm(primaryFormPath))


def getLoaderPrimaryForm() -> Loader:
    return LocalCache.load('loaderPrimaryForm', lambda: Loader(primaryForm=getPrimaryForm()))


def getGraph(degree) -> GraphModel:
    def _getGraph():
        from graph import GraphModel
        loader = getLoaderPrimaryForm()
        g = GraphModel(loader, degree)
        g.processGraphs(slice(51555))
        return g

    return LocalCache.load(f'graph{degree}', _getGraph)


@timeDec
def findBest(graphModelDegree, noteNumber):
    graph = getGraph(graphModelDegree)
    loader = getLoaderPrimaryForm()
    printSimilarText(noteNumber, graph.graphs, loader)


def main():
    findBestForNote0 = partial(findBest, noteNumber=0)
    findBestForNote0(graphModelDegree=1)
    findBestForNote0(graphModelDegree=2)
    findBestForNote0(graphModelDegree=3)
    findBestForNote0(graphModelDegree=4)


if __name__ == '__main__':
    main()
