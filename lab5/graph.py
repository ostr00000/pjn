from typing import List, TYPE_CHECKING

import networkx as nx
from scipy.sparse import vstack

from util import counterDecFactory

if TYPE_CHECKING:
    from loader import Loader


class GraphModel:

    def __init__(self, loader: 'Loader', degree=2):
        self.loader = loader
        self.degree = degree
        self.graphs = []

    def processGraphs(self, sliceObj=slice(200)):
        self.graphs = list(map(self._createGraph, self.loader.data[sliceObj]))
        self.graphs = vstack(self.graphs)

    @counterDecFactory(51555)
    def _createGraph(self, note: List[str]):
        graph = nx.DiGraph()

        maxRange = len(note)
        for start in range(maxRange):
            for end in range(start,
                             start + self.degree if start + self.degree < maxRange else maxRange):
                n1, n2 = note[start], note[end]
                try:
                    graph[n1][n2]['repeat'] += 1
                except KeyError:
                    graph.add_edge(n1, n2, repeat=1)

        sparseGraph = nx.to_scipy_sparse_matrix(graph, self.loader.nodelist)
        vectorFromMatrix = sparseGraph.reshape(len(self.loader.nodelist) ** 2)
        return vectorFromMatrix

    @property
    def vectors(self):
        return self.graphs

    def __str__(self):
        return f"Graph[degree={self.degree}]"


"""
from pympler import asizeof
asizeof.asizeof(sparseGraph)
Out[4]: 120200
asizeof.asizeof(graph)
Out[5]: 48088
asizeof.asizeof(sparseGraph.reshape((1, len(self.loader.nodelist)**2)))
Out[6]: 1584
"""
