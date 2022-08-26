"""Graph data structure and methods. Only the functionality needed for
RRWG is implemented.

"""
import numpy as np

class Graph():
    """Simple graph data structure.

    """
    def __init__(self, nvertices, complete=True,
                 self_loops=True, partition_size=0):
        """Create an instance of a Graph with n vertices. If the graph is
        complete, the edges are automatically created. If the vertices have
        self-loops, they are added automatically too.

        nvertices (int): number of vertices
        complete (bool): graph is complete?
        self_loops (bool): all vertices have self-loops?

        """
        self._adjs = {}
        self._n = nvertices
        self._complete = complete
        self._selfloops = self_loops
        self._partsize = partition_size

        # Initialize
        for i in range(self._n):
            self._adjs[i] = []

        # Add self-loops
        if self._selfloops:
            for i in range(self._n):
                self.add_edge(i, i)

        # All graphs are undirected
        if self._complete is True:
            for i in range(self._n):
                for j in range(self._n):
                    if i==j:
                        continue
                    self.add_edge(i, j)

    def add_edge(self, i: int, j: int):
        """Add an edge in the graph from i to j.

        """
        if j not in self._adjs[i]:
            self._adjs[i].append(j)
        if i not in self._adjs[j]:
            self._adjs[j].append(i)

    def vertices(self) -> list[int]:
        """Return an ordered list of vertices in the graph. All vertices are
        represented as integers as indices that start from zero.

        """
        return sorted(list(self._adjs.keys()))

    def neighbors(self, vert: int) -> list[int]:
        """Return an ordered list of vertices that are neighbors of the
        current vertex.

        """
        return sorted(list(self._adjs[vert]))

    def order(self) -> int:
        """Return the number of vertices in the graph.

        """
        return len(self._adjs)

    def partition(self, begin_vertex: int) -> list[int]:
        """Return an ordered list of vertices starting at begin_vertex and
        adding partsize vertices including begin_vertex. If the
        number of partitions is zero, all vertices are returned.

        """
        verts = self.vertices()
        if self._partsize == 0:
            return verts

        inf = begin_vertex
        sup = self._partsize
        return sorted(list(np.take(verts, range(inf, inf+sup),
                                   mode='wrap')))
