import unittest

from graph import Graph

N = 3
graph = Graph(N, npartitions=2)

for i in range(N):
    for j in range(i, N):
        graph.add_edge(i, j)

class TestNeighbor(unittest.TestCase):
    def runTest(self):
        errmsg = 'wrong neighbor vertex'
        verts = graph.neighbors(0)
        self.assertEqual(verts[0], 0, errmsg)
        self.assertEqual(verts[1], 1, errmsg)
        self.assertEqual(verts[2], 2, errmsg)
        
class TestPartition(unittest.TestCase):
    def runTest(self):
        errmsg = 'wrong partition vertex'
        verts = graph.partition(0)
        self.assertEqual(verts[0], 0, errmsg)
        self.assertEqual(verts[1], 1, errmsg)
        verts = graph.partition(1)
        self.assertEqual(verts[0], 1, errmsg)
        self.assertEqual(verts[1], 2, errmsg)
        verts = graph.partition(2)
        self.assertEqual(verts[0], 0, errmsg)
        self.assertEqual(verts[1], 2, errmsg)
