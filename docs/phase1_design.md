# Phase 1: Courier Problem Design and Planning

## Problem statement
Mini-Courier Planner is a Python desktop application that combines sorting,
dynamic programming, graph algorithms and an approximation technique to
prioritize parcels, select a feasible vehicle load and generate a delivery tour.

## Configuration
- Vehicle capacity: 100 kg
- Initial sample parcels: 20
- Locations: 5 (one depot and four delivery areas)
- Depot: D0 (Courier Depot)
- Distance unit: kilometres
- Parcel priority: integer from 1 to 10

## Parcel attributes
Each parcel stores a unique ID, recipient, destination ID, integer weight in kg,
priority score and delivery deadline in YYYY-MM-DD format.

## Graph model
The road network is an undirected, weighted graph represented by an adjacency
list. Vertices represent locations and non-negative edge weights represent
sample road distances in kilometres. Distances are illustrative, not live maps.

## Algorithm selection
1. Merge Sort orders parcels by descending priority, then earliest deadline,
   then parcel ID. Time: O(n log n); auxiliary space: O(n).
2. 0/1 Knapsack maximizes the sum of parcel priority scores subject to the
   vehicle capacity. With integer kilogram weights, time: O(nW) and space:
   O(nW), where n is the number of parcels and W is capacity.
3. Dijkstra calculates shortest paths in the non-negative weighted graph.
   With an adjacency list and binary min-heap: O((V+E) log V).
4. Nearest Neighbor TSP approximation repeatedly visits the closest unvisited
   required location and returns to the depot. With a distance matrix, its
   selection work is O(k^2), where k is the number of required locations.
   It does not guarantee an optimal TSP tour.

## Integrated workflow
Load parcel and graph JSON; validate inputs; sort parcels; run Knapsack; identify
the unique destinations of selected parcels; run Dijkstra from the depot and
each selected destination to construct shortest-path distances; run Nearest
Neighbor on this shortest-path distance matrix; expand the tour into road paths;
display selected parcels, load, route and total distance; benchmark algorithms.

## Assumptions and limitations
- One vehicle and one depot are considered.
- Parcel weights are whole kilograms for the DP table.
- Priority score is used as the Knapsack value; this is a simplified model.
- Sample road distances are fixed and illustrative.
- Nearest Neighbor is an approximation, not an exact TSP solver.
- The current model does not enforce time-window feasibility or traffic conditions.
