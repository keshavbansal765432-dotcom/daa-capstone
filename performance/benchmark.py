"""Command-line benchmark runner; writes performance/results.csv."""
import csv
import random
import time
from pathlib import Path

from algorithms.merge_sort import prioritize_parcels
from algorithms.knapsack import knapsack
from algorithms.dijkstra import dijkstra
from algorithms.nearest_neighbor import nearest_neighbor
from services import load_network

ROOT = Path(__file__).resolve().parents[1]


def run_benchmarks():
    rng = random.Random(42)
    rows = []

    for size in (20, 100, 500, 1000):
        parcels = [
            {"parcel_id": str(i), "priority_score": rng.randint(1, 10),
             "deadline": f"2026-12-{rng.randint(1, 28):02d}"}
            for i in range(size)
        ]
        start = time.perf_counter()
        prioritize_parcels(parcels)
        rows.append(("Merge Sort", size, time.perf_counter() - start))

    for size in (10, 20, 40, 80):
        parcels = [
            {"parcel_id": str(i), "weight_kg": rng.randint(1, 20),
             "priority_score": rng.randint(1, 10)}
            for i in range(size)
        ]
        start = time.perf_counter()
        knapsack(parcels, 100)
        rows.append(("0/1 Knapsack", size, time.perf_counter() - start))

    graph = load_network()["graph"]
    for vertex in graph:
        start = time.perf_counter()
        dijkstra(graph, vertex)
        rows.append(("Dijkstra", len(graph), time.perf_counter() - start))

    for size in (5, 10, 20, 40):
        nodes = [f"N{i}" for i in range(size)]
        matrix = {a: {b: (0 if a == b else abs(i-j)+1)
                      for j, b in enumerate(nodes)}
                  for i, a in enumerate(nodes)}
        start = time.perf_counter()
        nearest_neighbor(matrix, nodes[0])
        rows.append(("Nearest Neighbor", size, time.perf_counter() - start))

    output = ROOT / "performance" / "results.csv"
    output.parent.mkdir(exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["algorithm", "input_size", "runtime_seconds"])
        writer.writerows(rows)
    print(f"Saved {len(rows)} measurements to {output}")
    for algorithm, size, runtime in rows:
        print(f"{algorithm:20} n={size:4} runtime={runtime:.8f}s")


if __name__ == "__main__":
    run_benchmarks()
