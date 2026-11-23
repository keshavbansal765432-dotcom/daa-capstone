import unittest
from algorithms.knapsack import knapsack


class KnapsackTests(unittest.TestCase):
    def test_capacity_is_not_exceeded(self):
        parcels = [
            {"parcel_id":"A", "weight_kg":10, "priority_score":10},
            {"parcel_id":"B", "weight_kg":20, "priority_score":20},
            {"parcel_id":"C", "weight_kg":30, "priority_score":25}
        ]
        selected, weight, value = knapsack(parcels, 30)
        self.assertLessEqual(weight, 30)
        self.assertEqual(value, 30)
        self.assertEqual({p["parcel_id"] for p in selected}, {"A", "B"})

    def test_zero_capacity(self):
        selected, weight, value = knapsack(
            [{"parcel_id":"A", "weight_kg":1, "priority_score":5}], 0
        )
        self.assertEqual((selected, weight, value), ([], 0, 0))


if __name__ == "__main__":
    unittest.main()
