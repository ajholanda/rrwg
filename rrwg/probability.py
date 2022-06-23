
class Probability():
    """Transition probability class.

    """
    def __init__(self, rrwg, alpha: float, function='EXP'):
        """Initialize probability object with the reinforced factor alpha and
        the function chosen to be used in the calculation.

        """
        self._rrwg = rrwg
        self._alpha = alpha
        if func == 'EXP':
            self.__func = self.__exp
        elif func == 'POW':
            self.__func = self.__pow
        else:
            sys.exit('panic: unknown function \"{}\"'.format(func))

    
    def __exp(self, cur_walk: int, vert: int):
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

    def calc(self, walk: int, v_src: int, v_dest: int):
        """Calculate the probability of the walk to go from vertex v_src to
        the vertex v_dest.

        rrwg (RRWG): RRWG object
        walk (int): walk index
        v_src (int): vertex source index
        v_dest (int): vertex destination index

        """
        return self._func()
