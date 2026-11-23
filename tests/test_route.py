import unittest
from algorithms.nearest_neighbor import nearest_neighbor


class NearestNeighborTests(unittest.TestCase):
    def test_closed_tour(self):
        matrix = {
            "D0":{"D0":0, "L1":4, "L2":7},
            "L1":{"D0":4, "L1":0, "L2":2},
            "L2":{"D0":7, "L1":2, "L2":0}
        }
        route, distance = nearest_neighbor(matrix, "D0")
        self.assertEqual(route[0], "D0")
        self.assertEqual(route[-1], "D0")
        self.assertEqual(set(route[:-1]), {"D0", "L1", "L2"})
        self.assertEqual(distance, 13)


if __name__ == "__main__":
    unittest.main()
