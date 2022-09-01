#!/usr/bin/env python3
"""Main entry point to execute the simulations.

"""
import configparser
import os
import sys

from graph import Graph
from log import write as logwrite
from prob import Probability
from simul import simulate
from walk import Walk

# Load the setting from configuration file.
FILENAME = 'rrwg.conf'
config = configparser.ConfigParser()
if os.path.exists(FILENAME):
    config.read(FILENAME)
else:
    print('ERROR: Create a configuration file named "{}" '.format(FILENAME)+
          'in the current directory. \n'
          'See rrwg.conf.example in the project directory or '+
          'https://github.com/aholanda/rrwg/blob/main/rrwg.conf.example '+
          'for an example of configuration file.')
    sys.exit(-1)

if __name__ == "__main__":
    #Initialize a graph and walks after using the parameters from the
    #configuration file.
    walks = []

    if 'type' in config['default']:
        gtype = config['default']['type']
    else:
        MSG = """graph "type" is not defined in {}.
    Graph "type" should be:
    complete: complete graph with no partitions
    partitions: non-complete graph with partitions
    \t\tof complete subgraphs.""".format(FILENAME)
        sys.exit('panic: {}'.format(MSG))
    logwrite('type={}'.format(gtype))

    # Number of vertices
    if 'vertices' in config['default']:
        nverts = int(config['default']['vertices'])
    else:
        sys.exit('panic: number of "vertices" was not set in {}'
                 .format(FILENAME))
    logwrite('vertices={}'.format(nverts))

    if gtype == 'complete':
        func = config['default']['function']
        prob = Probability(func)

        graph = Graph(nverts)
        for i in graph.vertices():
            # The walk can traverse all vertices.
            walk = Walk(graph.vertices(), i)
            walks.append(walk)

    elif gtype == 'partitions':
        # For paritions function is always POWER
        prob = Probability('POW')

        if 'partition_size' in config['default']:
            partsize = int(config['default']['partition_size'])
        else:
            sys.exit('panic: "partition_size" was not set in {}.'
                     .format(FILENAME))

        if partsize > nverts:
            sys.exit('panic: number of partitions > number of vertices')

        graph = Graph(nverts, complete=False,
                      partition_size=partsize)
        for i in graph.vertices():
            # Each walk starts at the vertex with
            # the same id and the number of partitions
            # is the range where it can walk. For example,
            # a walk with id 2 starts at v2, and if the
            # number of partitions is 2, it can walk at
            # v2 and v3.
            # All subgraphs are complete.

            # Partitions in terms of vertices.
            part = graph.partition(i)
            # Make the edges
            for j in part:
                graph.add_edge(i, j)
            walk = Walk(part, i)
            walks.append(walk)
    else:
        sys.exit('panic: unknown graph type "{}" in {}'
                 .format(gtype, FILENAME))

    if 'alpha' in config['default']:
        prob.alpha = float(config['default']['alpha'])
    if 'epsilon' in config['default']:
        prob.epsilon = float(config['default']['epsilon'])
    logwrite('function={}\nalpha={}\nepsilon={}'
             .format(prob.function_name(),
                     prob.alpha,
                     prob.epsilon))

    if 'time' in config['default']:
        nsteps = int(config['default']['time'])
    else:
        sys.exit('panic: "time" steps was not set in {}.'
                 .format(FILENAME))

    SEED = None
    if 'seed' in config['default']:
        SEED = int(config['default']['seed'])

    simulate(nsteps, graph, walks, prob, SEED)
