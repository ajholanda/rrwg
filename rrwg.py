import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import sys
from igraph import Graph


# empty value is represented by NOVAL variable
NOVAL = -1


# Utils #
def eprint(s):
    print(s, file=sys.stderr)


class nop():
    def __init__(self):
        self.name = ''

    @staticmethod
    def eprint(s):
        pass

    def write(self, s):
        pass

    def close(self):
        pass


def fatal(msg):
    """Print an error message and exit.
    """
    msg = 'fatal: ' + msg
    eprint(msg)
    sys.exit(-1)


Vertex = int


class Graph():
    def __init__(self, nvertices):
        self._n = nvertices
        # Each vertex is identified by the index
        # of the list of adjacencies.
        self._adjs = []
        for _ in range(self._n):
            self._adjs.append([])

    def add_arc(self, u, v):
        if v not in self._adjs[u]:
            self._adjs[u].append(v)

    def get_neighbors(self, v) -> list:
        return self._adjs[v]

    def order(self) -> int:
        return self._n


class Walker():
    def __init__(self, idx, graph):
        self._id = idx
        self._graph = graph
        self._nvisits = [0] * self._graph.order()
        self._location = NOVAL
        self._total_visits = 0

    def get_nlocations(self) -> int:
        return self._graph.order()

    def get_location(self) -> Vertex:
        return self._location

    def get_locations(self):
        return [i for i in range(self.get_nlocations())]

    def set_location(self, location):
        self._location = location

    def get_nvisits(self, location):
        return self._nvisits[location]
    
    def get_total_visits(self):
        return self._total_visits

    def set_nvisits(self, location, value):
        self._nvisits[location] += value
        self._total_visits += value

    def __str__(self):
        return 'w{}'.format(self._id) 

    def visit(self, location):
        self.set_nvisits(location, 1)
        self.set_location(location)


class Walkers():
    def __init__(self, nwalkers, graph):
        self._graph = graph
        self._walkers = \
            [Walker(i, self._graph) for i in range(nwalkers)]

    def __getitem__(self, x) -> Walker:
        return self._walkers[x]

    def __len__(self):
        return len(self._walkers)

    def __str__(self):
        s = ''
        for w in self._walkers:
            s += str(w)
        return '[' + s + ']'


class RRWG():
    def __init__(self, filename, nolog=False, \
            quiet=False, sep='\t'):
        self._graph = None
        self._walkers = None
        self._nolog = nolog
        self._quiet = quiet
        self._sep = sep

        # I/O #
        # save the input file name
        self._infn = filename
        # use the file base name as identifier
        self._name = \
            os.path.splitext(os.path.basename(self._infn))[0]
        # read the input file and create the graph and walkers
        self.__read(filename)
        
        # open the log file
        logfn = self._name + '.log'
        if self._nolog:
            self._logf = nop()
            if os.path.exists(logfn):
                os.remove(logfn)
        else:
            self._logf = open(logfn, 'w')
        
        # assign the right warn function according 
        # to quiet state
        if self._quiet:
            self.warn = nop.eprint
        else:
            self.warn = eprint
    
    def get_nwalkers(self) -> int:
        return len(self._walkers)

    def __fclose(self, f):
        if f:
            f.close()
            if f.name:
                self.warn('* wrote {}'.format(f.name))

    def __read(self, filename):
        # list of lists with the initial number 
        # of visits by the walkers in the vertices
        lsts_vsts = []
        # lists of adjacencies before parsing
        lsts_adjs = []
        # mark used to identify the walker location in vertex
        loc_mark = '*'
        # row index
        i = 0
        # expected number of columns
        expected_ncols = 0
        f = open(self._infn, 'r')
        for row in f.readlines():
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
            if i == 0:
                # initialize the expected number of columns
                # to compare to the next rows
                expected_ncols = ncols
            
            # check if the number of columns is as expected
            if i > 0 and ncols != expected_ncols:
                fatal('{}.{}: wrong number of colums, expected {} not {}'.
                        format(filename, i+1, expected_ncols, ncols))

            # the first column has the list of adjacencies 
            # for the vertex i
            lsts_adjs.append(cols[0]) 

            # the rest of columns contains the number of visits
            # in the vertices for the walker where the column
            # number plus one represents the walker index 
            # and the row number the vertex index
            lsts_vsts.append(cols[1:])
            # increment row index
            i += 1
        f.close()

        # create the graph #
        # save the initial location of walkers
        # the number of lists is equal to the number of vertices
        nverts = len(lsts_adjs)        
        self._graph = Graph(nverts)
        for u, raw_adjs in enumerate(lsts_adjs):
            adjs = raw_adjs.split(",")
            for v in adjs:
                v = int(v)
                self._graph.add_arc(u, v)

        # create the walkers #
        # using the lists of visits
        nwalkers = len(lsts_vsts[0])
        self._walkers = Walkers(nwalkers, self._graph)
        inilocs = [NOVAL] * nwalkers
        for v, lst_vsts in enumerate(lsts_vsts):
            for wi, vsts in enumerate(lst_vsts):
                if vsts[0] == loc_mark:
                    if inilocs[wi] == NOVAL:
                        vsts = vsts[1:]
                        self._walkers[wi].set_location(v)
                    else:
                        fatal('{}: repeated location marker at column {}'.
                                format(filename, wi+1))
                self._walkers[wi].set_nvisits(v, int(vsts))
        self.__wp()

    def __wp(self):
        for wi, w in enumerate(self._walkers):
            loc = w.get_location()
            if loc is NOVAL:
                fatal('{}: initial location not set for walker {}'.
                        format(self._infn, wi))
        
            for v in w.get_locations():
                x = w.get_nvisits(v)
                if x < 0:
                    fatal('{}: wrong number of visits for walker {}, vertex {}'.
                            format(self._infn, wi, v))

    def __exp(self, factor) -> float:
        return math.exp(-self._alpha*factor)

    def __pow(self, factor) -> float:
        return factor - (self._graph.order()-factor)**self._alpha

    def calc_repellency(self, w, u, v, vs):
        # calculate the total repellency
        rsum = 0.0
        # repellency of analized vertex
        rv = 0.0

        totalvisits = float(w.get_total_visits())
        for x in vs:
            visits = float(w.get_nvisits(x))
            # separate the repellency the probably next
            # destination
            r = self._func(visits/totalvisits)
            rsum += r
            self._logf.write('\t\t\t\tr({},v{})={}({:.3f}*{:.0f}/{:.0f})={:.4f}\n'.
                    format(w, x, self._funcstr, self._alpha,\
                            visits, totalvisits, r))
            if x == v:
                rv = r

        # The current location of w must be summed to normalize
        # the repellency index
        visits = float(w.get_nvisits(u))
        r = self._func(visits/totalvisits)
        self._logf.write('\t\t\t\tr({},v{})={}({:.3f}*{:.0f}/{:.0f})={:.4f}\n'.
                format(w, u, self._funcstr, self._alpha,\
                        visits, totalvisits, r))
        rsum += r
        repel = rv/rsum
        self._logf.write('\t\t\tr(v{})/sum_r={:.3f}/{:.3f}={:.3f}\n'.
                    format(v, rv, rsum, repel))
        return repel

    def walk(self, nwalks, alpha, function="exp"):
        # open the output file
        outfn = self._name + '.dat'
        self._outf = open(outfn, 'w')
        
        # core parameters
        self._alpha = alpha
        self._nwalks = nwalks
        self._funcstr = function

        # check if the function to calculate the repellency
        # is declared
        if self._funcstr == "exp":
            self._func = self.__exp
        elif self.funcstr == "pow":
            self._func = self.__pow
        else:
            fatal('unknown function {}'.format(function))

        assert self._func is not None

        self._logf.write('# alpha={:.4f}\n'.format(self._alpha))
        self._logf.write('# nwalks={}\n'.format(self._nwalks))
        self._logf.write('# function={}\n'.format(self._funcstr))
        self._logf.write('# walkers={}\n'.format(self._walkers))
        for t in range(nwalks):
            self._logf.write('t={}\n'.format(t))
            for w in self._walkers:
                u = w.get_location()
                self._logf.write('  loc({})=v{}\n'.format(w, u))
                vs = self._graph.get_neighbors(u)
                # save transition probabilities for u to visit v
                # based on the others walkers
                probs = {}
                for v in vs:
                    r = 0.0
                    for ww in self._walkers:
                        if w == ww:
                            continue
                        r += self.calc_repellency(ww, u, v, vs)
                    probs[v] = r
                    self._logf.write('\t\tpr(v{})={:.3f}\n'.format(v, r))

                r = 0.0
                upper = sum(probs.values())
                rand =  random.uniform(0.0, upper)
                self._logf.write('\trandom/upper={:.3f}/{:.1f}'.
                        format(rand, upper))
                for v, pr in probs.items():
                    r += pr
                    if r > rand:
                        w.visit(v)
                        self._logf.write('\t => {} goto v{}\n\n'.format(w, v))
                        break

                self._logf.write('\t => visits({}) = {}\n\n'.format(w, w._nvisits))
            # write data
            self.__write()
        # close log and output files
        self.__fclose(self._logf)
        self.__fclose(self._outf)
        # plot curves for visits
        self.__plot()

    def __write(self):
        # line to be written
        line = []
        # enqueue columns from each walker
        cols = []
        for w in self._walkers:
            for v in range(w.get_nlocations()):
                visits = w.get_nvisits(v)
                cols.append(str(visits))
        # join all columns separated by sep
        line = self._sep.join(cols) + '\n'
        assert line
        self._outf.write(line)
        self._outf.flush()

    def __plot(self):
        labels = []
        plotfn = self._name + '.pdf'
        nw = self.get_nwalkers()
        nv = self._graph.order()
        xs = np.arange(self._nwalks)
        Y = np.zeros((self._nwalks, nw*nv), int)

        f = open(self._outf.name, 'r')
        for t, line in enumerate(f.readlines()):
            line = line.rstrip()
            cols = line.split(self._sep)
            for wi in range(nw):
                y = []
                for v in range(nv):
                    j = wi*nw + v
                    Y[t, j] = int(cols[j])
        f.close()

        fig, axs = plt.subplots(nw, sharex=True)
        fig.suptitle('Random Repelling Walks on Graphs')
        for wi in range(nw):
            for v in range(nv):
                j = wi*nw + v
                axs[wi].plot(xs, Y[:,j])
            axs[wi].set(ylabel = 'visits($w_{}$)'.format(wi))

        for v in range(nv):
            labels.append('$v_{}$'.format(v))
        fig.legend(axs, labels=labels)
        plt.xlabel('t')
        plt.show()
        fig.savefig(plotfn)
        self.warn('* wrote {}'.format(plotfn))


def usage(prog, flags):
    msg = 'usage: {} [ARGS] infile'.format(prog)
    eprint('{}\nARGS'.format(msg))
    for k, v in flags.items():
        eprint('\t {}: {}'.format(k, v[0]))


if __name__ == '__main__':
    argc = len(sys.argv)
    # file to read
    infn = None
    # arguments state
    ok = 1
    # map flags to their description and default state
    flags = {
            '--alpha': ['repellency coefficient', '-1.0'],
            '--function': \
                    ['[optional] function to calculate the repellency, '\
                    'options: exp (default), pow', 'exp'],
            '--nwalks': ['number of walks to perform', '-1'],
            '--nolog': ['[optional] do not write the log file', False],
            '--output': ['[optional] write the output to the specified file name, '\
                    'otherwise the prefix of input file name is used', None],
            '--quiet': ['[optional] turn off all warnings', False]
            }

    # evaluate input file name
    if argc > 1:
        i = 1
        while i < argc:
            arg = sys.argv[i]
            if i == argc-1:
                # ensure the input file name argument is not a flag
                if arg[:2] == '--':
                    break
                else:
                    infn = arg
                    ok <<= 1
            else:
                if arg in flags:
                    if arg == '--nolog' or arg == '--quiet':
                        flags[arg][1] = True
                    elif i+1 < argc:
                        parm = sys.argv[i+1]
                        if arg == '--alpha':
                            flags[arg][1] = float(parm)
                            ok <<= 1
                        elif arg == '--function':
                            flags[arg][1] = parm
                        elif arg == '--nwalks':
                            flags[arg][1] = int(parm)
                        else:
                            break
                        i += 1
                    else:
                        break

                else:
                    break
            i += 1

    if ok != 4:
        usage(sys.argv[0], flags)
        sys.exit(-1)

    rrwg = RRWG(infn, nolog=flags['--nolog'][1], \
            quiet=flags['--quiet'][1])
    rrwg.walk(flags['--nwalks'][1], \
            flags['--alpha'][1], \
            function=flags['--function'][1])
