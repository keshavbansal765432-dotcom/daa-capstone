# Algorithm Notes for Viva

## Merge Sort
Divide the list into halves until each part has at most one item. Merge the
halves in sorted order. The implementation is stable and uses a key of
(-priority_score, deadline, parcel_id).

## 0/1 Knapsack
For each parcel i and capacity c:
- Do not take it: dp[i-1][c]
- Take it if it fits: value[i] + dp[i-1][c-weight[i]]
Choose the maximum of the two. Backtrack through the DP table to recover
the selected parcel IDs. Each parcel is either selected once or not selected.

## Dijkstra
Initialize source distance to zero and all other distances to infinity.
Repeatedly extract the vertex with the smallest tentative distance. Relax each
outgoing edge. Non-negative weights are required.

## Nearest Neighbor TSP
Start at the depot. Repeatedly select the closest unvisited required destination.
After all required destinations have been visited, return to the depot. This is
a greedy heuristic and may produce a non-optimal tour.

## Complexity summary
- Merge Sort: O(n log n) time, O(n) auxiliary space.
- 0/1 Knapsack: O(nW) time and O(nW) space.
- Dijkstra with adjacency list and binary heap: O((V+E) log V).
- Nearest Neighbor with a distance matrix: O(k^2) time.
