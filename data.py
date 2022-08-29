"""Handle data operations like writing to a file.

"""
from walk import Walk

class Data():
    """Wrapper to output data.

    """
    def __init__(self, walks: list[Walk]):
        self._walks = walks
        self._fname = 'rrwg.dat'
        self._dataf = open(self._fname, 'w')
        for i, walk in enumerate(walks):
            for j in walk.vertices():
                self._dataf.write('\tw{}v{}'.format(i, j))
        self._dataf.write('\n')
        self.write()

    def __del__(self):
        if self._dataf:
            self._dataf.close()
        print('* Wrote {}'.format(self._fname))

    def write(self):
        """Write the current data saved in walk list
        to the output file.

        """
        for walk in self._walks:
            for i in walk.vertices():
                self._dataf.write('\t{}'.format(walk.nvisits(i)))
        self._dataf.write('\n')
        self._dataf.flush()
