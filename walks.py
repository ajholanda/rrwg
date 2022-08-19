"""Data representation of walks.

"""
import numpy as np

class Walk:
    """Data representation of walk.

    """
    def __init__(self, ident, nvertices: int, start_location: int):
        """Create an instance of walk data representation.

        ident (int): identification number
        start_location (int): current location of the walk in terms
        of vertices
        """
        self._id = ident
        # Save the number of visits in each vertex.
        # The default number of visits before the walk starts
        # is one.
        self._nvisits = np.full(nvertices, 1, dtype=int)
        # Save the current walk location.
        self._curloc = start_location

    def index(self):
        """Return the index of the current walk.

        """
        return self._id

    def cur_location(self) -> int:
        """Return the current location in terms of vertex.

        """
        return self._curloc

    def visit(self, vert: int):
        """Update the Walk variables when it visits a new location.

        """
        self._curloc = vert
        self._nvisits[vert] += 1
        # TODO: trace when a walk visit a new vertex
        #print('\t\t\t{}: {}'.format(self, self._nvisits))

    def nvisits(self, vert: int):
        """Return the number of visits in the vertex location by the current
        walk.


        vert (int): vertex location
        """
        return self._nvisits[vert]

    def __str__(self):
        return 'w{}'.format(self._id)

class Walks:
    """Walks is a placeholder for a set of Walk objects.

    """
    def __init__(self, nwalks: int, nvertices: int):
        """Data representation of the Walks.

        nwalks (int): number of walks to be initialized
        nvertices (int): the number of vertices in the graph used by
        the walks

        """
        self._walks = []
        self._nverts = nvertices
        self._i = 0

        for i in range(nwalks):
            # The walk is placed at the vertex index calculated as
            # walk index modulo the number of vertices.
            vert = i % nvertices
            self._walks.append(Walk(i, self._nverts, vert))

        assert len(self._walks) == nwalks

    def __len__(self):
        return len(self._walks)

    def get(self, walk: int) -> Walk:
        """Return the specified walk.
        """
        return self._walks[walk]

    def cur_location(self, walk) -> int:
        """Return the current walk location in terms of vertices.

        """
        return self._walks[walk].cur_location()

    def nvisits(self, walk, vert):
        """Mark a walk visitation.

        walk (int): index of the walk
        vert (int): index of the vertex visited

        """
        return self._walks[walk].nvisits(vert)

    def count_vertex_visits(self, vert) -> int:
        """Count the number of visits in the vertex vert.

        """
        nvis = 0
        for walk in self._walks:
            nvis += walk.nvisits(vert)

        return nvis

    def visit(self, walk, vert):
        """Mark a walk visitation.

        walk (int): index of the walk that is performing the visit
        vert (int): index of the vertex being visited

        """
        self._walks[walk].visit(vert)
