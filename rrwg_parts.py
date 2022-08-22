#!/usr/bin/env python3
"""Simulate the random reinforcing walks on graph
taking partitions of the graph. Each partition is a
complete graph.

"""
import numpy as np

from conf import config
from graph import Graph
from probability import Probability
from simul import simulate
from walk import Walk

def parts():
    """Execute the RRWG simulation on graph partitions.

    """
    nverts = int(config['default']['vertices'])
    nparts = int(config['default']['partitions'])
    nsteps = int(config['default']['time'])
    alpha = float(config['default']['alpha'])
    walks = []

    prob = Probability(alpha, 'POW')
    graph = Graph(nverts, complete=False)
    for i in graph.vertices():
        # Each walk starts at the vertex with
        # the same id and the number of partitions
        # is the range where it can walk. For example,
        # a walk with id 2 starts at v2, and if the
        # number of partitions is 2, it can walk at
        # v2 and v3.
        # All subgraphs are complete.

        # Partitions in terms of vertices.
        vparts = sorted(np.take(np.arange(graph.order())
                                , range(i, i+nparts)
                                , mode='wrap'))
        # Make the edges
        for j in vparts:
            graph.add_edge(i, j)
        walk = Walk(vparts, i)
        walks.append(walk)

    simulate(nsteps, graph, walks, prob)

if __name__ == '__main__':
    parts()
