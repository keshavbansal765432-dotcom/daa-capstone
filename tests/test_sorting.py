import unittest
from algorithms.merge_sort import merge_sort, prioritize_parcels


class MergeSortTests(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(merge_sort([5, 1, 4, 2, 3]), [1, 2, 3, 4, 5])

    def test_empty_and_single(self):
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([7]), [7])

    def test_parcel_priority_and_deadline(self):
        parcels = [
            {"parcel_id":"B", "priority_score":8, "deadline":"2026-11-20"},
            {"parcel_id":"A", "priority_score":8, "deadline":"2026-11-18"},
            {"parcel_id":"C", "priority_score":10, "deadline":"2026-11-22"}
        ]
        result = prioritize_parcels(parcels)
        self.assertEqual([p["parcel_id"] for p in result], ["C", "A", "B"])


if __name__ == "__main__":
    unittest.main()
