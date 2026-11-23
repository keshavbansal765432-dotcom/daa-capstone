"""Merge Sort implementation for parcel prioritization."""
from typing import Any, Callable, List, Optional


def merge_sort(items: List[Any], key: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    """
    Return a sorted copy of items using Merge Sort.

    The sort is stable. By default, values are compared directly.
    For parcels, pass a key such as:
        lambda p: (-p["priority_score"], p["deadline"], p["parcel_id"])
    """
    if key is None:
        key = lambda value: value

    def sort(values):
        if len(values) <= 1:
            return values[:]

        middle = len(values) // 2
        left = sort(values[:middle])
        right = sort(values[middle:])
        return merge(left, right)

    def merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            # <= preserves the original order when keys are equal.
            if key(left[i]) <= key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    return sort(list(items))


def prioritize_parcels(parcels):
    """Higher priority first, then earlier deadline, then parcel ID."""
    return merge_sort(
        parcels,
        key=lambda p: (
            -int(p["priority_score"]),
            str(p["deadline"]),
            str(p["parcel_id"])
        )
    )
