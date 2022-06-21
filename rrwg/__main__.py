#!/usr/bin/env python3

from graph import Graph
from walks import Walks

class RRWG():
    def __init__(self, graph: Graph, walks: Walks):
        self._graph = graph
        self._walks = walks

    def walk(self, tmax: int):
        for _ in range(tmax):
            for walk in self._walks:
                print(walk)

if __name__ == '__main__':
    G = Graph(3)
    W = Walks(2)
    rrwg = RRWG(G, W)
    rrwg.walk(2)
