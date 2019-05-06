import os
from functools import partial

from cache import LocalCache
from compare import printSimilarText
from graph import GraphModel
from loader import Loader
from primary_form import PrimaryForm
from tf_idf import TfidfModel
from util import timeDec

primaryFormPath = os.path.join('data', 'odm.txt')


def getPrimaryForm() -> PrimaryForm:
    return LocalCache.load('primaryForm', lambda: PrimaryForm(primaryFormPath))


def getLoaderPrimaryForm() -> Loader:
    return LocalCache.load('loaderPrimaryForm', lambda: Loader(primaryForm=getPrimaryForm()))


def getGraph(degree) -> GraphModel:
    def _getGraph():
        loader = getLoaderPrimaryForm()
        g = GraphModel(loader, degree)
        g.processGraphs(slice(51555))
        return g

    return LocalCache.load(f'graph{degree}', _getGraph)


def getTfIdfModel() -> TfidfModel:
    def _tfIdf():
        loader = getLoaderPrimaryForm()
        tfidf = TfidfModel(loader)
        tfidf.calcVector()
        return tfidf

    return LocalCache.load("tfidf", _tfIdf)


@timeDec
def findBestInTfIdfModel(noteNumber):
    model = getTfIdfModel()
    printSimilarText(noteNumber, model.vectors, model.loader)


@timeDec
def findBestInGraphModel(graphModelDegree, noteNumber):
    graph = getGraph(graphModelDegree)
    printSimilarText(noteNumber, graph.graphs, graph.loader)


def main():
    noteNumber = 0
    findBestInTfIdfModel(noteNumber)

    findBestForNote0 = partial(findBestInGraphModel, noteNumber=noteNumber)
    findBestForNote0(graphModelDegree=1)
    findBestForNote0(graphModelDegree=2)
    findBestForNote0(graphModelDegree=3)
    findBestForNote0(graphModelDegree=4)


if __name__ == '__main__':
    main()
