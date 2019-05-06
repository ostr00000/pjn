from functools import partial

from accessFunctions import getTfIdfModel, getGraph
from compare import printSimilarText, printResultFromAllModels, scoreModels
from util import timeDec


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
    # main()
    # printResultFromAllModels()
    scoreModels()
