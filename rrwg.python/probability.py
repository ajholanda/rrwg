"""This module is used in the RRWG simulation to calculate the
probability of a walk w located in a vertex u to go to a neighbor v of
u, taking into account the number of visits of the other walks in the
vertex v. The walk w tends to go to the vertex less visited by the
other walks.

"""
import math
import sys

from rrwg.walks import Walks

def vertex_count_visits(walks: Walks, vert: int) -> int:
    """Count the number of visits of all walks in the specified vertex.

    walks (Walks): placeholder object for all walks
    vert (int): vertex to count the visits

    """
    return walks.count_vertex_visits(vert)

def sum_norm_vertex_visits_from_other_walks(walks: Walks, \
                                            cur_walk: int,
                                            vert: int) -> float:
    """Sum of the normalized number of visits from all walks
    excepting the current walk to the specified vertex.

    walks (Walks): placeholder for the walk objects
    cur_walk (int): index of the current walk
    vert (int): vertex eligible to be visited

    """
    # Accumulator of the normalized number of visits from the
    # walks, excepting the current walk.
    acc = 0.0

    # Total number of visits in the vertex vert
    total_nvis = vertex_count_visits(walks, vert)

    for walk in range(len(walks)):
        if walk == cur_walk: # ignore current walk
            continue

        norm_nvis = \
            float(walks.get(walk).nvisits(vert)) / total_nvis
        acc += norm_nvis

    return acc

class Probability():
    """Transition probability class.

    """
    def __init__(self, alpha: float, function='EXP'):
        """Initialize probability object with the reinforced factor alpha and
        the function chosen to be used in the calculation.

        """
        self._alpha = alpha
        if function == 'EXP':
            self.__func = self.__exp
        elif function == 'POW':
            self.__func = self.__pow
        else:
            sys.exit('panic: unknown function \"{}\"'.format(function))


    def __exp(self, walks: Walks, cur_walk: int, vert: int):
        """Apply the exponential function to the number of visits and the
        reinforcing factor alpha.

        """
        acc = \
            sum_norm_vertex_visits_from_other_walks(walks, cur_walk, vert)

        prob = math.exp(-self._alpha * acc)

        # TODO: put print() into log file
        #print('\t\tEXP: w{}, v{}={}'.format(cur_walk, vert, prob))
        return prob

    def __pow(self, walks: Walks, cur_walk: int, vert: int):
        """Apply a factor to a power function of the number of visits and the
        reinforcing factor alpha.

        """
        # Total number of visits in the vertex vert
        total_nvis = vertex_count_visits(walks, vert)

        # Normalized number of visits of the current walk.
        norm_nvis_cur_walk = \
            walks.get(cur_walk).nvisits(vert) / total_nvis

        acc = \
            sum_norm_vertex_visits_from_other_walks(walks, cur_walk, vert)

        prob = norm_nvis_cur_walk * pow(len(walks) - acc, self._alpha)

        # TODO: put print() into log file
        #print('\t\tPOW: w{}, v{}={}'.format(cur_walk, vert, prob))
        return prob

    def calculate(self, walks: Walks, cur_walk: int, \
                  v_dest: int) -> float:
        """Calculate the transition probability of the current walk that are
        located at source vertex to go to destination vertex.

        walks (Walks): Walks object to access data
        from each walk
        cur_walk (Walk): current walk
        v_src (int): source vertex
        v_dest (int): destination vertex

        """
        return self.__func(walks, cur_walk, v_dest)
