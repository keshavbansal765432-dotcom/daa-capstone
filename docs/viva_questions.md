# Viva Preparation

1. Why is Merge Sort suitable? It guarantees O(n log n) worst-case time.
2. Is Merge Sort stable? Yes; equal keys retain their relative order.
3. What does 0/1 mean in Knapsack? Each parcel is either selected once or not selected.
4. What is the Knapsack objective? Maximize total priority value without exceeding capacity.
5. What does a DP state represent? The best value using the first i parcels and capacity c.
6. Why use Dijkstra? It finds shortest paths when edge weights are non-negative.
7. Can Dijkstra handle negative edges? No.
8. What is an adjacency list? A representation storing each vertex's neighbors and edge weights.
9. Does Nearest Neighbor guarantee optimal TSP? No; it is an approximation heuristic.
10. Why use shortest-path distances before TSP? The route heuristic should compare actual shortest road distances between required stops.
11. What does time.perf_counter measure? High-resolution elapsed wall-clock time.
12. Why test multiple input sizes? To observe how runtime changes as input size grows.
13. Why is Knapsack O(nW)? There are n+1 rows and W+1 capacity states, each computed in constant time.
14. What are the model's limitations? One vehicle, fixed sample distances, no traffic or time-window constraints.
