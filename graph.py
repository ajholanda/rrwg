"""Graph data structure and methods. Only the functionality needed for
RRWG is implemented.

"""
class Graph():
    """Simple graph data structure.

    """
    def __init__(self, nvertices, complete=True, self_loops=True):
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

    def add_edge(self, i, j):
        """Add an edge in the graph from i to j.

        """
        self._adjs[i].append(j)

    def vertices(self) -> [int]:
        """Return the set of vertices in the graph. All vertices are
        represented as integers as indices that start from zero.

        """
        return set(self._adjs.keys())

    def neighbors(self, vert):
        """Return a list of vertices that are neighbors of the current vertex.

        """
        return set(self._adjs[vert])

    def order(self) -> int:
        """Return the number of vertices in the graph.

        """
        return len(self._adjs)
