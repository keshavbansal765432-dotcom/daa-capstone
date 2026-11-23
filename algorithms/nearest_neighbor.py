"""Nearest Neighbor heuristic for an approximate TSP tour."""


def nearest_neighbor(distance_matrix, start):
    """
    Build a closed approximate tour from start.

    distance_matrix is a nested dictionary:
        distances["D0"]["L1"] == shortest road distance D0 -> L1

    Returns (route, total_distance). Every other vertex is visited once,
    then the route returns to start. This is an approximation, not an
    optimal-TSP guarantee.
    """
    if start not in distance_matrix:
        raise ValueError(f"Unknown starting location: {start}")

    unvisited = set(distance_matrix.keys())
    unvisited.discard(start)
    route = [start]
    total_distance = 0
    current = start

    while unvisited:
        reachable = [
            (distance_matrix[current][candidate], candidate)
            for candidate in unvisited
            if candidate in distance_matrix[current]
        ]
        if not reachable:
            raise ValueError("Not all delivery locations are reachable from the current location.")
        distance, next_location = min(reachable, key=lambda item: (item[0], item[1]))
        if distance == float("inf"):
            raise ValueError("The delivery graph contains an unreachable location.")
        total_distance += distance
        route.append(next_location)
        unvisited.remove(next_location)
        current = next_location

    if len(route) > 1:
        return_distance = distance_matrix[current][start]
        if return_distance == float("inf"):
            raise ValueError("Cannot return to the starting depot.")
        total_distance += return_distance
        route.append(start)

    return route, total_distance
