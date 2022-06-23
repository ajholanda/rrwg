#!/usr/bin/env python3
"""We implement the vertex-Reinforced Random Walks on Graphs (RRWG)
simulation as defined in
[Rosales, 2022](https://www.sciencedirect.com/science/article/pii/S0304414922000631).

"""
import math
import sys

import numpy as np

from graph import Graph
from walks import Walks
from plot import plot

__version__ = '20220622'

EXP, POW = 0, 1

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

    def pr_exp(self, cur_walk: int, vert: int):
        """Apply the exponential function to the number of visits and the
        reinforcing factor alpha.

        """
        pr_w = 0.0
        acc = 0.0

        # Total number of visits in the vertex vert
        total_nvis = self._walks.count_vertex_visits(vert)

        for walk in range(self._m):
            norm_nvis = \
                self._walks.get(walk).nvisits(vert) / total_nvis

            prob = math.exp(- self._alpha * norm_nvis)
            if walk == cur_walk: # ignore current walk
                pr_w = prob
            acc += prob

        assert pr_w != 0.0
        pr_w = pr_w / acc
        print('\t\t__exp: w{}, v{}={}'.format(cur_walk, vert, pr_w))
        return pr_w

    def pr_pow(self, cur_walk: int, vert: int):
        """Apply a factor to a power function of the number of visits and the
        reinforcing factor alpha.

        """
        factor = self.count_visits(cur_walk, vert)

        return factor * \
            pow(self._m - self.sum_count_visits(cur_walk, vert),
                self._alpha)

    def calc_prob(self, cur_walk, v_src, v_dest):
        """Calculate the transition probability of the current walk that are
        located at source vertex to go to destination vertex.

        cur_walk (Walk): current walk
        v_src (int): source vertex
        v_dest (int): destination vertex

        """
        # The values from the time step before the current
        # are used to calculate the probability.
        pr_v = 0.0
        pr_sum = 0.0

        for vert in self._graph.neighbors(v_src):
            prob = self._func(cur_walk, vert)
            pr_sum += prob

            if vert == v_dest:
                pr_v = prob

        return pr_v/pr_sum

    def walk(self, nsteps: int, alpha: float, func='EXP'):
        """Start the walking stopping after a number of steps.

        nsteps (int): the number of steps to walk
        alpha (float): reinforcing factor
        func (function): function to apply in the transition
        probability calculation

        """
        self._alpha = alpha
        # Count t=0 plus the next steps
        self._nsteps = nsteps + 1
        if func == 'EXP':
            self._func = self.pr_exp
        elif func == 'POW':
            self._func = self.pr_pow
        else:
            sys.exit('panic: unknown function \"{}\"'.format(func))

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
                    probs[v_dest] = self.calc_prob(walk, v_src, v_dest)

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
                        print('\trand={:.3f}, w{} goto v{}'
                              .format(rand, walk, v_dest))
                        break
            # Update visits
            for walk in range(self._m):
                v_next_dest = locs[walk]
                self._walks.visit(walk, v_next_dest)

def print_banner(rwg: RRWG):
    msg = 'RRWG(v{}): '.format(__version__)
    msg += '|W|={}, |V|={}, alpha={}\n'\
        .format(rwg.nwalks(), rwg.nvertices(), rwg.alpha())

    print(msg)

if __name__ == '__main__':
    args = {
        'alpha': 1.0
        , 'function': 'EXP'
        , 'nverts': 2
        , 'nwalks': 2
        , 'nsteps': 3
    }

    for i in range(1, len(sys.argv), 2):
        flag, arg = sys.argv[i:i+2]
        if flag == '-a':
            args['alpha'] = float(arg)
        elif flag == '-f':
            args['function'] = arg.upper()
        elif flag == '-t':
            args['nsteps'] = int(arg)
        elif flag == '-v':
            args['nverts'] = int(arg)
        elif flag == '-w':
            args['nwalks'] = int(arg)
        else:
            sys.exit('panic {} {}'.format(flag, arg))

    G = Graph(args['nverts'])
    W = Walks(args['nwalks'], G.order())
    rrwg = RRWG(G, W)
    rrwg.walk(args['nsteps'], args['alpha'], args['function'])
    plot(rrwg, 'Title')
    print_banner(rrwg)
