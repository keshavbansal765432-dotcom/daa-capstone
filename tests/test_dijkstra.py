import unittest
from algorithms.dijkstra import dijkstra, reconstruct_path


class DijkstraTests(unittest.TestCase):
    def test_shortest_path(self):
        graph = {
            "A":[("B", 4), ("C", 1)],
            "B":[("A", 4), ("C", 2), ("D", 1)],
            "C":[("A", 1), ("B", 2), ("D", 5)],
            "D":[("B", 1), ("C", 5)]
        }
        distances, previous = dijkstra(graph, "A")
        self.assertEqual(distances["D"], 4)
        self.assertEqual(reconstruct_path(previous, "A", "D"), ["A", "C", "B", "D"])

    def test_negative_edge_rejected(self):
        with self.assertRaises(ValueError):
            dijkstra({"A":[("B", -1)], "B":[("A", -1)]}, "A")


if __name__ == "__main__":
    unittest.main()
