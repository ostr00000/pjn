from typing import List, TYPE_CHECKING

import networkx as nx

from lab5.util import counterDecFactory

if TYPE_CHECKING:
    from loader import Loader


class GraphModel:

    def __init__(self, loader: 'Loader', degree=2):
        self.loader = loader
        self.degree = degree
        self.graphs = []

    def processGraphs(self, sliceObj=slice(200)):
        self.graphs = list(map(self._createGraph, self.loader.data[sliceObj]))

    @counterDecFactory(50_000)
    def _createGraph(self, note: List[str]):
        graph = nx.DiGraph()

        maxRange = len(note)
        for start in range(len(self.loader.words)):
            for end in range(start,
                             start + self.degree if start + self.degree < maxRange else maxRange):
                n1, n2 = note[start], note[end]
                try:
                    graph[n1][n2]['repeat'] += 1
                except KeyError:
                    graph.add_edge(n1, n2, repeat=1)

        return graph
