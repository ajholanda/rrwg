#!/usr/bin/env python3
"""We implement the vertex-Reinforced Random Walks on Graphs (RRWG)
simulation as defined in
[Rosales, 2022](https://www.sciencedirect.com/science/article/pii/S0304414922000631).

"""
import numpy as np

from graph import Graph
from probability import Probability

def simulate(nsteps: int, graph: Graph, walks, prob: Probability):
    """Start the walking stopping after a number of steps.

    nsteps (int): the number of steps to walk
    alpha (float): reinforcing factor
    func (function): function to apply in the transition
    probability calculation

    """
    for _ in range(nsteps):
        # Save the next vertex destination for the walks
        # to update the number of visits at once.
        locs = {}

        for walk in walks:
            # Initialize the array of probability transitions
            # of w goto v with zeros.
            probs = np.zeros(graph.order())

            v_src = walk.cur_location()
            neighbs =  graph.neighbors(v_src)
            for v_dest in neighbs:
                probs[v_dest] = \
                    prob.calculate(walks, walk, v_dest)

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
        for walk in walks:
            v_next_dest = locs[walk]
            walk.visit(v_next_dest)
