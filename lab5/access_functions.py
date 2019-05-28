import os

from cache import LocalCache
from graph import GraphModel
from loader import Loader
from primary_form import PrimaryForm
from tf_idf import TfidfModel

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


def getAllModels():
    return [
        getTfIdfModel(),
        getGraph(1),
        getGraph(2),
        getGraph(3),
        getGraph(4),
    ]
