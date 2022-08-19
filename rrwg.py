#!/usr/bin/env python3
"""We implement the vertex-Reinforced Random Walks on Graphs (RRWG)
simulation as defined in
[Rosales, 2022](https://www.sciencedirect.com/science/article/pii/S0304414922000631).

"""
import sys

import numpy as np

from rrwg.graph import Graph
from rrwg.walks import Walks
from rrwg.output import plot, save
from rrwg.probability import Probability

__version__ = '20220624'
__file__ = sys.argv[0]

# Default arguments for the flags
args = {
    'alpha': 1.0
    , 'function': 'EXP'
    , 'nverts': 2
    , 'nwalks': 2
    , 'nsteps': 3
}


class RRWG():
    """The RRWG class is a placeholder for the procedures to perform the
    RRWG simulation.

    """

    def __init__(self, graph: Graph, walks: Walks):
        """Create an instance of RRWG with the Graph to be traversed by the
        Walks.

        """
        self._graph = graph
        # Number of vertices
        self._n = graph.order()
        self._walks = walks
        # Number of walks
        self._m = len(walks)
        # Initialize reinforcing function and properties
        self._func = None
        self._alpha = 1.0
        # Location to save the number of visits
        self._nvisits = np.full((self._m, self._n), 1, dtype=int)
        # Number of steps to perform
        self._nsteps = 0

    def alpha(self) -> float:
        """Return the reinforced factor

        """
        return self._alpha

    def nvertices(self) -> int:
        """Return the number of vertices used in the simulation.

        """
        return self._graph.order()

    def walks(self) -> Walks:
        """Return the Walks object.

        """
        return self._walks

    def nwalks(self) -> int:
        """Return the number of walks used in the simulation.

        """
        return len(self._walks)

    def nsteps(self) -> int:
        """Return the number of steps.

        """
        return self._nsteps

    def walk(self, nsteps: int, alpha: float, func='EXP'):
        """Start the walking stopping after a number of steps.

        nsteps (int): the number of steps to walk
        alpha (float): reinforcing factor
        func (function): function to apply in the transition
        probability calculation

        """
        # Count t=0 plus the next steps
        self._nsteps = nsteps + 1
        prob = Probability(alpha, func)

        for _ in range(1, self._nsteps):
            # Save the next vertex destination for the walks
            # to update the number of visits at once.
            locs = np.full(self._m, -1, dtype=int)

            for walk in range(self._m):
                # Initialize the array of probability transitions
                # of w goto v with zeros.
                probs = np.zeros(self._n)

                v_src = self._walks.cur_location(walk)
                neighbs =  self._graph.neighbors(v_src)
                for v_dest in neighbs:
                    probs[v_dest] = \
                        prob.calculate(self._walks, walk, v_dest)

                # Sum the transition probabilies
                probs_sum = np.sum(probs)
                # Generate a random number between 0.0 and probs_sum
                rand = np.random.uniform(0.0, probs_sum)
                # Choose the next vertex destination
                probs_sum = 0.0
                for v_dest in neighbs:
                    probs_sum += probs[v_dest]
                    if probs_sum > rand:
                        locs[walk] = v_dest
                        # TODO: put tracing of steps for the walks
                        #print('\trand={:.3f}, w{} goto v{}'
                        #      .format(rand, walk, v_dest))
                        break
            # Update visits
            for walk in range(self._m):
                v_next_dest = locs[walk]
                self._walks.visit(walk, v_next_dest)

def print_banner(rwg: RRWG):
    """Print core information about the program.

    """
    msg = 'RRWG(version: {}): '.format(__version__)
    msg += '|W|={}, |V|={}, alpha={}\n'\
        .format(rwg.nwalks(), rwg.nvertices(), rwg.alpha())
    print(msg, file=sys.stderr)

def print_usage_and_exit():
    """Print how to use the program and exit.

    """
    msg = 'usage: {} [options]\n'.format(__file__)
    msg += ' options:\n'
    msg += '   -a alpha (float), default={}\n'.format(args['alpha'])
    msg += \
        '   -d number of vertices (int), default={}\n' \
        .format(args['nverts'])
    msg += \
        '   -m number of walks (int), default={}\n' \
        .format(args['nwalks'])
    msg += \
        '   -n number of time steps (int), default={}\n' \
        .format(args['nsteps'])
    msg += \
        '   -p function to plug into transition\n' \
        '      probability calculation (EXP|POW),\n'\
        '      default={}\n'.format(args['function'])

    print(msg, file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    if (len(sys.argv) - 1) % 2 != 0:
        print_usage_and_exit()

    for i in range(1, len(sys.argv), 2):
        flag, arg = sys.argv[i:i+2]
        if flag == '-a':
            args['alpha'] = float(arg)
        elif flag == '-f':
            args['function'] = arg.upper()
        elif flag == '-n':
            args['nsteps'] = int(arg)
        elif flag == '-d':
            args['nverts'] = int(arg)
        elif flag == '-m':
            args['nwalks'] = int(arg)
        else:
            print_usage_and_exit()

    G = Graph(args['nverts'])
    W = Walks(args['nwalks'], G.order())
    rrwg = RRWG(G, W)
    rrwg.walk(args['nsteps'], args['alpha'], args['function'])
    plot(rrwg, 'Random vertex-Reinforced Walk')
    save(rrwg)
    print_banner(rrwg)
