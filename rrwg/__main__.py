#!/usr/bin/env python3
"""We implement the vertex-Reinforced Random Walks on Graphs (RRWG)
simulation as defined in
[Rosales, 2022](https://www.sciencedirect.com/science/article/pii/S0304414922000631).

"""
import math
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

    def count_visits(self, cur_walk: int, vert: int):
        """Return the number of visits of walk w to vertex v normalized by the
        total number of visits in v.

        """
        cur_walk_nvisits = 0
        # sum all visits at the vertex v
        vsum = 0
        for walk in range(self._m):
            nvis = self._walks.nvisits(walk, vert)
            if walk == cur_walk:
                cur_walk_nvisits = nvis
            vsum += nvis

        return float(cur_walk_nvisits)/vsum

    def sum_count_visits(self, cur_walk: int, vert: int):
        """Sum all the visits of all walks excepting the the current walk in
        the vertex specified.

        cur_walk: current walk
        vert: vertex to count the visits
        """
        acc = 0.0

        # Traverse the other walks
        for walk in range(self._m):
            if walk == cur_walk: # ignore current walk
                continue
            acc += self.count_visits(walk, vert)
        return acc

    def __exp(self, cur_walk: int, vert: int):
        """Apply the exponential function to the number of visits and the
        reinforcing factor alpha.

        """
        acc = self.sum_count_visits(cur_walk, vert)
        print('\t\t__exp: {}, v{}={}'.format(cur_walk, vert, acc))
        return math.exp(-self._alpha*acc)

    def __pow(self, cur_walk: int, vert: int):
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

    def walk(self, nsteps: int, alpha: float, func=EXP):
        """Start the walking stopping after a number of steps.

        nsteps (int): the number of steps to walk
        alpha (float): reinforcing factor
        func (function): function to apply in the transition
        probability calculation

        """
        self._alpha = alpha
        # Count t=0 plus the next steps
        self._nsteps = nsteps + 1
        if func == EXP:
            self._func = self.__exp
        else:
            self._func = self.__pow

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
                        print('\tR={:.3f}, {} goto v{}'
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
    G = Graph(2)
    W = Walks(2, G.order())
    rrwg = RRWG(G, W)
    print_banner(rrwg)
    rrwg.walk(2, 1.)
    plot(rrwg, 'Title')
