#!/usr/bin/env python3
"""Simulate the random reinforcing walks on graph
taking partitions of the graph. Each partition is a
complete graph.

"""
from conf import config
from graph import Graph
from probality import Probability
from simul import simulate
from walks import Walk, Walks

def parts():
    for key in config.keys():
        nverts = int(config[key]['vertices'])
        nparts = int(config[key]['partitions'])
        nsteps = int(config[key]['time'])
        alpha = float(config[key]['alpha'])
        walks = []

        prob = Probability(alpha, 'POW')
        graph = Graph(nverts, complete=False)
        for i in g.vertices():
            # Each walk starts at the vertex with
            # the same id and the number of partitions
            # is the range where it can walk. For example,
            # a walk with id 2 starts at v2, and if the
            # number of partitions is 2, it can walk at
            # v2 and v3.
            # All subgraphs are complete.

            # Partitions in terms of vertices.
            vparts = np.arange(graph.order(),
                               np.arange(i, i+nparts+1),
                               mode='wrap')
            w = Walk(vparts, i)
            walks.append(w)

        simulate(nsteps, graph, walks, prob)

if __name__ == '__main__':
    parts()
