"""Data representation of walks.

"""

from graph import Vertex

class Walk:
    """Data representation of walk.

    """
    def __init__(self, ident, curr_location=None):
        """Create an instance of walk data representation.

        ident (int): identification number
        curr_location (Vertex): current location of the walk
        """
        self._id = ident
        self._curloc = curr_location

    def curr_location(self) -> Vertex:
        """Return the current location (Vertex).

        """
        return self._curloc

    def visit(self, loc: Vertex):
        """Update the Walk variables when it visits a new location.

        """
        self._curloc = loc

    def __str__(self):
        return 'w{}'.format(self._id)

class Walks:
    """Walks is a placeholder for a set of Walk objects.

    """
    def __init__(self, nwalks: int, start_locs=None):
        """Data representation of the Walks.

        nwalks (int): number of walks to be initialized

        """
        self._n = nwalks
        self._walks = []
        self._i = 0

        for i in range(self._n):
            vert = None
            if start_locs is not None:
                vert = start_locs[i]
            self._walks.append(Walk(i, vert))

    def __len__(self):
        return self._n

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < self._n:
            _w = self._walks[self._i]
            self._i += 1
            return _w

        raise StopIteration
