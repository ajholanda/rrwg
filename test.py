import unittest

from rrwg import RRWG

class TestWalk(unittest.TestCase):
    def test_attrs(self):
        rrwg = RRWG('example.rwg', quiet=True)
        rrwg.walk(1, 0.1)

        self.assertEqual(rrwg._graph.order(), 3)
        self.assertEqual(len(rrwg._walkers), 3)

if __name__ == '__main__':
    unittest.main
