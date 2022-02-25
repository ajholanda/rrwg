#!/usr/bin/env python3
"""
RRWG simulates the walkers' repelling random walks
on graphs. In this simulation, each walker has higher
probability to visit the vertices which have been
less visited by the other walkers.
"""

import math
import os
import random
import sys
import matplotlib.pyplot as plt
import numpy as np

# empty value is represented by NOVAL variable
NOVAL = -1

# Accuracy for the calculations
EPS=0.001


# Utils #
def eprint(string):
    """Print the string to standard error output.
    """
    print(string, file=sys.stderr)


def fatal(msg):
    """Print an error message and exit.
    """
    msg = 'fatal: ' + msg
    eprint(msg)
    sys.exit(-1)


Vertex = int


class Graph():
    """A graph is composed of vertices that are connected
    by edges. The vertices indices are mapped to the indices
    of the adjacency list and element of the list is an array
    with the vertices indices that are connected to current
    index in the array where the elements were inserted.
    """
    def __init__(self, nvertices):
        self._n = nvertices
        # Each vertex is identified by the index
        # of the list of adjacencies.
        self._adjs = []
        for _ in range(self._n):
            self._adjs.append([])

    @staticmethod
    def create_graph(list_of_adjacencies):
        """Create a graph from a list of adjacencies
        represented as string with the vertices
        indices separated by comma. For example:
            [
             "1,2,3", # neighbors of v0
             "0,2,3", # neighbors of v1
             "0,1,3",   # neighbors of v2
             "0,1,2"    # neighbors of v3
            ]
        """
        # The number of lists is equal to the number of vertices.
        nverts = len(list_of_adjacencies)
        graph = Graph(nverts)
        for _u, adjstr in enumerate(list_of_adjacencies):
            adjs = adjstr.split(",")
            for _v in adjs:
                _v = int(_v)
                graph.add_arc(_u, _v)
        return graph

    def add_arc(self, src, dst):
        """Add an arc from source src to the
        destination dst. The dst is the vertex
        index to be appended in the list of
        adjacencies at position src.
        """
        if dst not in self._adjs[src]:
            self._adjs[src].append(dst)

    def get_neighbors(self, src) -> list:
        """Return all neighbors (list of adjacencies)
        connected to the vertex src.
        """
        return self._adjs[src]

    def order(self) -> int:
        """Return the number of vertices in the graph.
        """
        return self._n

    def __str__(self):
        verts = []
        edges = []
        for v_count, adjs in enumerate(self._adjs):
            verts.append('v' + str(v_count))
            for j in adjs:
                edges.append('(v' + str(v_count) + ',v' + str(j) +')')
        return 'G={V={' + ','.join(verts) + '},E={' + ','.join(edges) + '}}'


class Walker():
    """Class to define the walkers that are used in the
    walks on the graph.
    """
    def __init__(self, idx, graph):
        # The walker identification.
        self._id = idx
        # The graph containing the vertices to be visited.
        self._graph = graph
        # Save the number of visits indexed by the
        # vertex index.
        self._nvisits = [0] * self._graph.order()
        # Location (vertex index) where the current
        # walker object is visiting.
        self._location = NOVAL
        # All visits performed by the current
        # walker object.
        self._total_visits = 0

    def get_nlocations(self) -> int:
        """Return the number of different locations
        (vertices) where the walker already has visited.
        """
        return self._graph.order()

    def get_location(self) -> Vertex:
        """Return the location (vertex) where the
        current walker object is visiting.
        """
        return self._location

    def get_locations(self):
        """Return the locations (vertices) that was or may
        be visited.
        """
        return list(range(self.get_nlocations()))

    def set_location(self, location):
        """Mark the location (vertex) where the current walker
        object is visiting.
        """
        self._location = location

    def get_nvisits(self, location):
        """Return the number of visits for the current
        walker object occurred in the location.
        """
        return self._nvisits[location]

    def get_total_visits(self):
        """Return the total number of visits performed
        by the current walker object.
        """
        return self._total_visits

    def set_nvisits(self, location, value):
        """Assign a value of visits for the current
        walker object in the location.
        """
        self._nvisits[location] += value
        self._total_visits += value

    def __str__(self):
        return 'w{}'.format(self._id)

    def visit(self, location):
        """When the current walker object performs
        a visit to location the number of visits to
        the location must be incremented and the current
        place of the walker must be updated.
        """
        self.set_nvisits(location, 1)
        self.set_location(location)


class Walkers():
    """Class Walkers works as a list of Walkers to
    facilitate the handling of multiple walkers'
    objects.
    """
    def __init__(self, nwalkers, graph):
        self._graph = graph
        self._walkers = \
            [Walker(i, self._graph) for i in range(nwalkers)]

    def __getitem__(self, idx) -> Walker:
        return self._walkers[idx]

    def __len__(self):
        return len(self._walkers)

    def __str__(self):
        names = []
        for widx in self._walkers:
            names.append(str(widx))
        return '{' + ', '.join(names) + '}'


class Writer():
    """Behavior wraps the possible changes of states
    by the objects that use it. The states are related
    to internal state and external interactions as I/O
    operations.
    """
    def __init__(self):
        # Default values for initialization.
        self._name = 'anonymous'
        self._is_verbose = True
        self._has_log = True
        self._logf = None
        self._sep = ' '
        # Data file handles
        self._files = {'log': None, 'dat': None}

    def get_name(self):
        """Return the name of the current Writer object.
        """
        return self._name

    def set_name(self, name: str):
        """Set the current object Writer identifier.
        """
        self._name = name

    def get_separator(self) -> str:
        """Return the column separator used by Writer
        instance.
        """
        return self._sep

    def set_separator(self, value: str):
        """Assign the string to be used as separator
        for columns in the Writer instance.
        """
        self._sep = value

    def get_file(self, kind: str):
        """Return the file handle associated
        with kind.
        """
        assert kind
        _file = self._files[kind]
        assert _file
        return _file

    def get_filename(self, kind: str) -> str:
        """Return the file name of the file associated
        with kind.
        """
        return self.get_file(kind).name

    def write(self, string: str, kind: str):
        """Print the string to the proper file.
        """
        if kind == "log":
            if self._has_log:
                if not self._files[kind]:
                    self._files[kind] = open(self._name + '.' + kind, 'w')
                self._files[kind].write(string)
        elif kind == "dat":
            if not self._files[kind]:
                self._files[kind] = open(self._name + '.' + kind, 'w')
            self._files[kind].write(string)
        else:
            fatal('unkown Writer kind: {}'.format(kind))

    def __del__(self):
        for _file in self._files.values():
            if _file:
                _file.close()
                eprint('* Wrote {}'.format(_file.name))


class RRWG():
    """The Random Repelling Walks on Graphs attributes
    and operations are implemented in RRWG. The class
    uses the Graph, Walker and Walkers classes to provide
    abstractions to be manipulated in a higher level.
    """
    def __init__(self):
        # Graph is initialized latter.
        self._graph = None
        # Walkers are initialized latter.
        self._walkers = None
        # Create Writer object to interact with I/O.
        self._writer = Writer()
        # Number of walks to perform.
        self._nwalks = NOVAL
        # Repelling coefficient.
        self._alpha = NOVAL
        # Name of repelling function.
        self._funcstr = None
        # Repelling function.
        self._func = None

    def get_nwalkers(self) -> int:
        """Return the number of walkers in the RRWG
        instance.
        """
        return len(self._walkers)

    def read(self, filename, sep='\t'):
        """Read the input file used to describe the
        graph, the walkers and the number of visites
        already performed by the walkers in the vertices.
        See man for more details about the file format.
        """
        # use the file base name as identifier
        name = \
            os.path.splitext(os.path.basename(filename))[0]
        # Set the name of writer object with the same name
        # as RRWG.
        self._writer.set_name(name)
        # Set separator for fields to be written in data file.
        self._writer.set_separator(sep)
        # list of lists with the initial number
        # of visits by the walkers in the vertices
        lsts_vsts = []
        # lists of adjacencies before parsing
        lst_adjs = []
        # mark used to identify the walker location in vertex
        loc_mark = '*'
        # read the input file and create the graph and walkers
        # expected number of columns
        expected_ncols = 0
        # Row (no comments) counter.
        row_count = 0
        infile = open(filename, 'r')
        for row in infile.readlines():
            # ignore empty lines and comments
            if not row or row[0] == '#':
                continue
            # remove new line
            row = row.rstrip()
            # split columns separated by space
            cols = row.split()
            # number of columns
            ncols = len(cols)
            # check for empty columns
            if ncols < 1:
                fatal('{}.{}: empty line'.format(filename, i+1))
            elif ncols == 1:
                fatal('{}.{}: no walker defined'.format(filename, i+1))
            else:
                pass
            if row_count == 0:
                # initialize the expected number of columns
                # to compare to the next rows
                expected_ncols = ncols
            # check if the number of columns is as expected
            if row_count > 0 and ncols != expected_ncols:
                fatal('{}.{}: wrong number of colums, expected {} not {}'.
                        format(filename, row_count+1, expected_ncols, ncols))

            # the first column has the list of adjacencies
            # for the vertex i
            lst_adjs.append(cols[0])

            # the rest of columns contains the number of visits
            # in the vertices for the walker where the column
            # number plus one represents the walker index
            # and the row number the vertex index
            lsts_vsts.append(cols[1:])
            # increment row index
            row_count += 1
        infile.close()

        self._graph = Graph.create_graph(lst_adjs)

        # create the walkers #
        # using the lists of visits
        nwalkers = len(lsts_vsts[0])
        self._walkers = Walkers(nwalkers, self._graph)
        inilocs = [NOVAL] * nwalkers
        for _v, lst_vsts in enumerate(lsts_vsts):
            for _wi, vsts in enumerate(lst_vsts):
                if vsts[0] == loc_mark:
                    if inilocs[_wi] == NOVAL:
                        vsts = vsts[1:]
                        self._walkers[_wi].set_location(_v)
                    else:
                        fatal('{}: repeated location marker at column {}'.
                                format(filename, _wi+1))
                self._walkers[_wi].set_nvisits(_v, int(vsts))
        self.__wp(filename)

    def __wp(self, fname):
        for _wi, _w in enumerate(self._walkers):
            loc = _w.get_location()
            if loc is NOVAL:
                fatal('{}: initial location not set for walker {}'.
                        format(fname, _wi))
            for _v in _w.get_locations():
                _x = _w.get_nvisits(_v)
                if _x < 0:
                    fatal('{}: wrong number of visits for walker {}, vertex {}'.
                            format(fname, _wi, _v))

    def __exp(self, factor) -> float:
        return math.exp(-self._alpha*factor)

    def __pow(self, factor) -> float:
        return factor - (self._graph.order()-factor)**self._alpha

    def calc_repellency(self, walker, vertv, u_neighbors):
        """Calculate the repellency
        """
        # calculate the total repellency
        rsum = 0.0
        # repellency of analized vertex
        repelv = 0.0

        totalvisits = float(walker.get_total_visits())
        for vertx in u_neighbors:
            visits = float(walker.get_nvisits(vertx))
            # separate the repellency the probably next
            # destination
            repel = self._func(visits/totalvisits)
            rsum += repel
            self._writer.write('\t\t\t\tr({},v{})={}({:.3f}*{:.0f}/{:.0f})={:.4f}\n'.
                    format(walker, vertx, self._funcstr, self._alpha,\
                            visits, totalvisits, repel), "log")
            if vertx == vertv:
                repelv = repel

        repel = repelv/rsum
        self._writer.write('\t\t\tr(v{})/sum_r={:.3f}/{:.3f}={:.3f}\n'.
                    format(vertv, repelv, rsum, repel), "log")
        return repel

    def walk(self, nwalks: int, alpha: float, function="exp"):
        """This method starts the repelling walks.

        Parameters:
        -----------
        nwalks (int): number of walks to perform.

        alpha (float): repelling coefficient.

        function (str): function to be used in the repelling
        index calculation.
        """
        # core parameters
        self._alpha = alpha
        self._nwalks = nwalks
        if self._nwalks < 1:
            fatal('The number of --nwalks must be greater than 1.')
        self._funcstr = function
        # check if the function to calculate the repellency
        # is declared
        if self._funcstr == "exp":
            self._func = self.__exp
        elif self._funcstr == "pow":
            self._func = self.__pow
        else:
            fatal('unknown function {}'.format(function))

        assert self._func is not None

        self._writer.write('# alpha={:.4f}\n'.format(self._alpha), "log")
        self._writer.write('# nwalks={}\n'.format(self._nwalks), "log")
        self._writer.write('# function={}\n'.format(self._funcstr), "log")
        self._writer.write('# walkers={}\n'.format(self._walkers), "log")
        self._writer.write('# {}\n'.format(self._graph), "log")
        for time in range(nwalks):
            self._writer.write('t={}\n'.format(time), "log")
            for walker in self._walkers:
                vertu = walker.get_location()
                self._writer.write('  loc({})=v{}\n'.format(walker, vertu), "log")
                u_neighbors = self._graph.get_neighbors(vertu)
                # Save transition probabilities for vertex u
                # to visit vertex v based on the others walkers.
                probs = {}
                for vertv in u_neighbors:
                    repel = 0.0
                    for reklaw in self._walkers:
                        if walker == reklaw:
                            continue
                        repel += self.calc_repellency(walker, vertv, u_neighbors)
                    probs[vertv] = repel
                    self._writer.write('\t\tpr(v{})={:.3f}\n'
                            .format(vertv, repel), "log")

                rcum = 0.0
                one = sum(probs.values())
                assert one >= 1.0-EPS
                assert one <= one+EPS
                rand =  random.uniform(0.0, one)
                self._writer.write('\trandom_number/one={:.3f}/{:.1f}={:.3f}'.
                        format(rand, one, rand/one), "log")
                for verti, prob in probs.items():
                    rcum += prob
                    if rcum > rand:
                        walker.visit(verti)
                        self._writer.write('\t => {} goto v{}\n\n'
                                .format(walker, verti), "log")
                        break

                self._writer.write('\t => visits({}) = {}\n\n'
                        .format(walker, walker.get_nvisits(verti)), "log")
            # write data
            self.__write()
        # plot curves for visits
        self.__plot()

    def __write(self):
        for walker in self._walkers:
            total_visits = walker.get_total_visits()
            for loci in range(walker.get_nlocations()):
                # Normalized visits
                frac_visits = walker.get_nvisits(loci) / float(total_visits)
                self._writer.write('{:.3f}\t'.format(frac_visits), "dat")
        self._writer.write('\n', "dat")

    def __plot(self):
        # Labels for the curves.
        labels = []
        # Plot file name.
        plotfn = self._writer.get_name() + '.pdf'
        # Number of walkers.
        nwalkers = self.get_nwalkers()
        # Number of vertices.
        nverts = self._graph.order()
        # Array to save time.
        xxs = np.arange(self._nwalks)
        # Matrix nwalkers x nverts.
        mat = np.zeros((self._nwalks, nwalkers*nverts), float)

        # Close data file to flush data.
        self._writer.get_file('dat').close()
        datafile = open(self._writer.get_filename('dat'), 'r')
        for ln_count, line in enumerate(datafile.readlines()):
            line = line.rstrip()
            cols = line.split(self._writer.get_separator())
            for w_count in range(nwalkers):
                for v_count in range(nverts):
                    col = w_count*nwalkers + v_count
                    mat[ln_count, col] = float(cols[col])
        datafile.close()

        fig, axs = plt.subplots(nwalkers, sharex=True)
        fig.suptitle('Random Repelling Walks on Graphs')
        for w_count in range(nwalkers):
            for v_count in range(nverts):
                col = w_count*nwalkers + v_count
                axs[w_count].plot(xxs, mat[:, col])
            axs[w_count].set(ylabel = 'visits($w_{}$)'.format(w_count))
            axs[w_count].set_ylim([0.0, 1.0])

        for vertv in range(nverts):
            labels.append('$v_{}$'.format(vertv))
        fig.legend(labels=labels)
        plt.xlabel('t')
        plt.show()
        fig.savefig(plotfn)
        eprint('* Wrote {}'.format(plotfn))


def print_usage(prog, pflags):
    """Print information about how to use the program.
    """
    msg = 'usage: {} [ARGS] infile'.format(prog)
    eprint('{}\nARGS:'.format(msg))
    for k, vals in pflags.items():
        eprint('\t {}: {}'.format(k, vals[0]))


if __name__ == '__main__':
    # Mark if the program is prepared to run.
    run = True
    # Counter for mandatory flags.
    mand_count = 0
    # File to read.
    input_fn = None
    # Map flags to their description and default state.
    flags = {
            '--alpha': ['repellency coefficient', '-1.0'],
            '--function': \
                    ['[optional] function to calculate the repellency, '\
                    'options: exp (default), pow', 'exp'],
            '--nwalks': ['number of walks to perform', '-1'],
            }

    if len(sys.argv)-1 not in (5,7):
        run = False
    else:
        input_fn = sys.argv[len(sys.argv)-1]
        for i in range(1, len(sys.argv)-1, 2):
            flag = sys.argv[i]
            if flag in flags.keys():
                flags[flag][1] = sys.argv[i+1]
                if flag in ('--alpha', '--nwalks'):
                    mand_count += 1
            else:
                run = False
                break

    if mand_count != 2:
        run = False

    if run:
        rrwg = RRWG()
        rrwg.read(input_fn)
        rrwg.walk(int(flags['--nwalks'][1]), \
                float(flags['--alpha'][1]), \
                function=flags['--function'][1])
    else:
        print_usage(sys.argv[0], flags)
        sys.exit(-1)
