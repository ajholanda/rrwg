#!/usr/bin/env python3
"""We implement the vertex-Reinforced Random Walks on Graphs (RRWG)
simulation as defined in
[Rosales, 2022](https://www.sciencedirect.com/science/article/pii/S0304414922000631).

"""
import numpy as np

from data import Data
from graph import Graph
from log import write as logwrite
from prob import Probability
from walk import Walk

def has_loc(vert: int, walks: list[Walk]) -> list[Walk]:
    """Return a list of walks whose vertex vert is a possible location to
    go.

    """
    mates =[]
    for walk in walks:
        if vert in walk.vertices():
            if walk not in mates:
                mates.append(walk)

    assert len(mates) > 0
    return mates

def simulate(nsteps: int, graph: Graph,
             walks: list[Walk], prob: Probability):
    """Start the walking stopping after a number of steps.

    nsteps (int): the number of steps to walk
    alpha (float): reinforcing factor
    func (function): function to apply in the transition
    probability calculation

    """
    # Write walks info to log file
    for count, walk in enumerate(walks):
        logwrite('loc(w{}, t=0)=v{}'.format(count, walk.cur_location()))
        logwrite('G(w{})={}'.format(count, walk.vertices()))

    data = Data(walks)
    for i in range(1, nsteps+1):
        logwrite('t={}'.format(i))
        # Save the next vertex destination for the walks
        # to update the number of visits at once.
        locs = {}

        for count, walk in enumerate(walks):
            # Initialize the array of probability transitions
            # of w goto v with zeros.
            probs = np.zeros(graph.order())

            v_src = walk.cur_location()
            logwrite('  loc(w{})=v{}'.format(count, v_src))
            for v_dest in list(graph.neighbors(v_src)):
                # Select the walks that has the destination vertex as
                # a possible location to walk.
                walks_v_dest = has_loc(v_dest, walks)

                probs[v_dest] = prob.calculate(walks_v_dest, walk, v_dest)
                logwrite('\tPr(w{}, v{})={}'
                         .format(count, v_dest, probs[v_dest]))

            # Sum the transition probabilies
            probs_sum = np.sum(probs)
            # Generate a random number between 0.0 and probs_sum
            rand = np.random.uniform(0.0, probs_sum)
            # Choose the next vertex destination
            probs_sum = 0.0
            for v_dest in graph.neighbors(v_src):
                probs_sum += probs[v_dest]
                if probs_sum > rand:
                    locs[walk] = v_dest
                    # Log next step
                    logwrite('\t\trand={:.3f}, w{} goto v{}'
                             .format(rand, count, v_dest))
                    break
        # Update visits
        for walk in walks:
            v_next_dest = locs[walk]
            walk.visit(v_next_dest)

        data.write()
