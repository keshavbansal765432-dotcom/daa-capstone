"""0/1 Knapsack dynamic programming implementation."""
from typing import Dict, List, Tuple


def knapsack(parcels: List[Dict], capacity: int) -> Tuple[List[Dict], int, int]:
    """
    Select parcels to maximize total priority_score without exceeding capacity.

    Parcel weights must be whole-number kilograms for this DP-table version.
    Returns (selected_parcels, total_weight, total_value).
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    normalized = []
    for parcel in parcels:
        weight = int(parcel["weight_kg"])
        value = int(parcel["priority_score"])
        if weight <= 0:
            raise ValueError(f'Parcel {parcel["parcel_id"]} must have positive weight.')
        if value < 0:
            raise ValueError(f'Parcel {parcel["parcel_id"]} cannot have negative priority.')
        normalized.append((weight, value))

    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, value = normalized[i - 1]
        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]
            if weight <= current_capacity:
                candidate = value + dp[i - 1][current_capacity - weight]
                if candidate > dp[i][current_capacity]:
                    dp[i][current_capacity] = candidate

    selected_indices = []
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            selected_indices.append(i - 1)
            remaining -= normalized[i - 1][0]

    selected_indices.reverse()
    selected = [parcels[i] for i in selected_indices]
    total_weight = sum(int(p["weight_kg"]) for p in selected)
    total_value = sum(int(p["priority_score"]) for p in selected)
    return selected, total_weight, total_value


def build_dp_table(parcels: List[Dict], capacity: int):
    """Return the complete DP table for teaching/demo purposes."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, parcel in enumerate(parcels, start=1):
        weight = int(parcel["weight_kg"])
        value = int(parcel["priority_score"])
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if weight <= cap:
                dp[i][cap] = max(dp[i][cap], value + dp[i - 1][cap - weight])
    return dp
