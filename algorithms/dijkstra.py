"""Dijkstra shortest-path algorithm using an adjacency list and min-heap."""
import heapq
import math


def dijkstra(graph, start):
    """
    Return (distances, previous).

    graph format:
        {"D0": [("L1", 12), ("L2", 18)], ...}

    All edge weights must be non-negative.
    """
    if start not in graph:
        raise ValueError(f"Unknown start vertex: {start}")

    for source, neighbors in graph.items():
        for destination, weight in neighbors:
            if weight < 0:
                raise ValueError("Dijkstra cannot process negative edge weights.")
            if destination not in graph:
                raise ValueError(f"Unknown vertex {destination!r} connected from {source!r}.")

    distances = {vertex: math.inf for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        if current_distance != distances[current_vertex]:
            continue

        for neighbor, edge_weight in graph[current_vertex]:
            new_distance = current_distance + edge_weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def reconstruct_path(previous, start, destination):
    """Reconstruct a shortest path from a Dijkstra previous-vertex map."""
    if destination not in previous:
        return []
    path = []
    current = destination
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous[current]
    if not path or path[-1] != start:
        return []
    return list(reversed(path))
