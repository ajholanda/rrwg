import math
import sys
from igraph import Graph


def fatal(msg):
    msg = 'fatal: ' + msg
    print(msg, file=sys.stderr)
    sys.exit(-1)


class Walker(object):
    count = 0

    def __init__(self):
        # where the walker starts
        self._location = None
        # store the visited vertices
        self._path = []
        # map vertex to the number of visits
        self._visits = {}

    def __str__(self):
        return 'location={}'.format(self._location) + ', '\
            'visits={}'.format(self._visits)

    def add_to_path(self, location):
        self._path.append(self._location)

    def is_path_empty(self):
        return len(self._path) == 0

    def get_cur_location(self):
        return self._location

    def set_cur_location(self, location):
        self._location = location

    def get_locations(self):
        return self._visits.keys()

    def get_nlocations(self):
        return len(self._visits)

    def get_nvisits(self, v):
        return self._visits[v]

    def set_nvisits(self, v, value):
        self._visits[v] = value

    def visit(self, v):
        self._visits[v] += 1
        self._location = v
        self.add_to_path(v)


def check_input_postconditions(filename, walkers):
    for i, w in enumerate(walkers):
        loc = w.get_cur_location()
        if loc is None:
            fatal('{}: initial location not set for walker {}'.
                    format(filename, i+1))
        
        for v in w.get_locations():
            x = w.get_visits(v)
            if x is None or x < 1:
                fatal('{}.{}: wrong visits value at column {}'.
                        format(filename, j+1, i+1))


def read_walkers_settings(filename, graph):
    visits = []
    locations = None
    # mark used to identify the walker location in vertex
    loc_mark = '*'
    # row counter
    row_count = 0
    # expected number of columns (walkers)
    expected_ncols = 0
    f = open(filename, 'r')
    for row_count, row in enumerate(f.readlines()):
        # remove new line
        row = row.rstrip()
        # ignore empty lines
        if not row:
            continue
        # split columns separated by space
        cols = row.split()
        # number of columns (walkers)
        ncols = len(cols)
        # check for empty columns
        if ncols < 1:
            fatal('{}.{}: empty line'.format(filename, row_count+1))
        # initialize locations in the first row (line)
        if row_count == 0:
            walkers = [] 
            for i in range(ncols):
                walkers.append(Walker())
            # initialize the expected number of columns
            # to compare in the next rows
            expected_ncols = ncols

        # check if the number of columns is as expected
        if row_count > 0 and ncols != expected_ncols:
            fatal('{}.{}: wrong number of colums, expected {} not {}'.
                    format(filename, row_count+1, expected_ncols, ncols))

        # traverse the columns (walkers)
        for col_count, col in enumerate(cols):
            visits = -1
            v = graph.vs[row_count]
            # location mark must be the 1st character
            if col[0] == loc_mark:
                if walkers[col_count].is_path_empty():
                    # set the row count (vertex) as initial location
                    visits = int(col[1:])
                    walkers[col_count].set_cur_location(v)
                else:
                    fatal('{}.{}: repeated location marker at column {}'.
                            format(filename, row_count+1, col_count+1))
            else:
                visits = int(col)
            walkers[col_count].set_visits(v, visits)
    f.close()
    check_input_postconditions(filename, walkers)
    return walkers



def _exp(fraction, alpha, nverts):
    return math.exp(-alpha*fraction)


def _pow(fraction, alpha, nverts):
    return factor * (nverts)**alpha


class RRWG:
    def __init__(self, basename):
        # read pajek file with the graph description
        fn = basename + '.net'
        self._g = Graph.Read_Pajek(fn)

        fn = basename + '.ini'
        self._walkers = read_walkers_settings(fn, self._g)

    def get_nvertices(self):
        return self._g.vcount()

    def check_preconditions(self):
        nverts_net = self.get_nvertices()
        nverts_ini = self._walkers[0].get_nlocations()

        # 1. Check if the number of vertices in the graph
        # is equal to the number of vertices in the initialization
        # file (.ini).
        if nverts_net != nverts_ini:
            fatal('the number of vertices differs in .net={} and .ini={} files'.
                    format(nverts_net, nverts_ini))

    def begin(self, nwalks, alpha, function="exp"):
        func = None

        self.check_preconditions()

        if function == "exp":
            func = _exp
        elif function == "pow":
            func = _pow
        else:
            fatal('unknown function {}'.format(function))

        assert func is not None

        for t in range(nwalks):
            for w in self._walkers:
                u = w.get_cur_location()
                for v in u.neighbors():
                    # assess the other walkers visits in the 
                    # u's neighbor v
                    for x in self._walkers:
                        if x == w:
                            continue
                        count += x.get_nvisits(v)

                


if __name__ == '__main__':
    rrwg = RRWG('rrwg.tmp/a')
    rrwg.begin(2, .1)
