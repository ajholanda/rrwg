"""Data representation of walks.

"""
class Walk:
    """Data representation of walk.

    """
    def __init__(self, vertices: list[int], start_location: int):
        """Create an instance of walk data representation.

        vertices (list[int]): the vertices index where the walk is
                              allowed to visit.
        start_location (int): current location of the walk in terms
        of vertices
        """
        self._vertices = vertices
        # Save the number of visits in each vertex.
        # The default number of visits before the walk starts
        # is one.
        self._nvisits = {}
        # Initialize the number of visits per vertex
        for i in vertices:
            if i == start_location:
                self._nvisits[i] = 1
            else:
                self._nvisits[i] = 1
        # Save the current walk location.
        self._curloc = start_location

    def vertices(self):
        """Return the vertices where the walk is allowed to go.

        """
        return self._vertices

    def cur_location(self) -> int:
        """Return the current location in terms of vertex.

        """
        return self._curloc

    def visit(self, vert: int):
        """Update the Walk variables when it visits a new location.

        """
        self._curloc = vert
        self._nvisits[vert] += 1

    def nvisits(self, vert: int) -> int:
        """Return the number of visits in the vertex location by the current
        walk.


        vert (int): vertex location
        """
        if vert not in self._nvisits:
            return 0
        return self._nvisits[vert]

    def total_visits(self) -> int:
        """Return the total number of visits by the current
        walk in all vertices that it can go to.
        """
        acc = 0

        for nvis in self._nvisits.values():
            acc += nvis

        return acc

class Walks:
    """Walks is a placeholder for a set of Walk objects.

    """
    def __init__(self):
        """Data representation of the Walks.

        nwalks (int): number of walks to be initialized
        nvertices (int): the number of vertices in the graph used by
        the walks

        """
        self._walks = []
        self._i = 0

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
