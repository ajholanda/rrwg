import math
import sys
from igraph import Graph

# empty value is represented by EMPTY variable
EMPTY = -1

# no value assigned is represented by NOVAL variable
NOVAL = -1

# X save the number of visits of the walkers
# X is a matrix where the column number is the vertex index
# and the row number is the walker index, then
# X[0,1] saves the number of visits of walker 0 to 
# the vertex 1.
X = np.array(int)

# Save the current location of a walker where
# the array index is mapped to walker index and 
# the content is the vertex index.
wlocs = []

# number of walkers
NW = EMPTY

# number of vertices
NV = EMPTY

def fatal(msg):
    """Print an error message and exit.
    """
    msg = 'fatal: ' + msg
    print(msg, file=sys.stderr)
    sys.exit(-1)


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
    for y, row in enumerate(f.readlines()):
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
        # initialize matrix of visits with the first walker (row)
        if y == 0:
            # create and initialize the first row of the visits matrix
            X = np.array(np.zeros(ncols, int))
            # initialize variable that saves the number of walkers
            # with the number of columns in the first row
            NW = ncols
            # initialize the expected number of columns
            # to compare to the next rows
            expected_ncols = ncols
        # check if the number of columns is as expected
        if y > 0 and ncols != expected_ncols:
            fatal('{}.{}: wrong number of colums, expected {} not {}'.
                    format(filename, x+1, expected_ncols, ncols))

        # traverse the columns (walkers)
        for x, col in enumerate(cols):
            v = graph.vs[row_count]
            # location mark must be the 1st character
            if col[0] == loc_mark:
                if L[x] == EMPTY:
                    # set the column number (vertex) as initial location
                    L[x] = y
                    # remove the location mark and set the initial
                    # number of visits for the walker x to 
                    # the vertex y
                    X[x, y] = int(col[1:])
                else:
                    fatal('{}.{}: repeated location marker at column {}'.
                            format(filename, row_count+1, col_count+1))
            else:
                X[x, y] = int(col)
    # the number of vertices is equal to the number of rows plus one
    NV = y + 1
    f.close()
    # X.size saves the number of columns (walkers)
    assert NW != X.size
    # X.ndim saves the number of rows (vertices)
    assert NV != X.ndim
    check_input_postconditions(filename, X)


def _exp(x):
    assert ALPHA != NOVAL
    return math.exp(-ALPHA*x)


def _pow(x):
    assert ALPHA != NOVAL
    return x * (NV-x)**ALPHA


def walk(filename, nwalks, alpha, function="exp"):
    ALPHA = alpha
    # function to be applied to the visits and calculate 
    # repellency
    func = None
    # read pajek file with the graph description
    fn = basename + '.net'
    self._g = Graph.Read_Pajek(fn)

    # read init file with the initial number of visits 
    # of the walkers and their initial position
    fn = basename + '.ini'
    self._walkers = read_walkers_settings(fn, self._g)

    # check preconditions
    nverts_net = self.get_nvertices()
    nverts_ini = self._walkers[0].get_nlocations()

    # 1. Check if the number of vertices in the graph
    # is equal to the number of vertices in the initialization
    # file (.ini).
    if nverts_net != nverts_ini:
        fatal('the number of vertices differs in .net={} and .ini={} files'.
                format(nverts_net, nverts_ini))

    # check if the function to calculate the repellency
    # is declared
    if function == "exp":
        func = _exp
    elif function == "pow":
        func = _pow
    else:
        fatal('unknown function {}'.format(function))

    assert func is not None

    # in the matrix of visits X
    # walk nwalks times
    for t in range(nwalks):
            # traverse the walkers indices
            for x in range(NW):
                # initialize the probabilities for walker x
                # to go to the next vertex y
                probs = np.zeros(X.ndim)
                # sum all visits for the walkers
                S = np.sum(X, axis=0)
                # get the current location for walker x
                u = L[x]
                for v in u.neighbors():
                    # assess the other walkers visits in the 
                    # u's neighbor v
                    for w in range(NW):
                        if w == x:
                            continue
                        

if __name__ == '__main__':
    walk('rrwg.tmp/a', 2, .1)
