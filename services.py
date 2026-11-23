"""Application-level data loading, validation, and courier planning."""
import json
from pathlib import Path

from algorithms.merge_sort import prioritize_parcels
from algorithms.knapsack import knapsack
from algorithms.dijkstra import dijkstra, reconstruct_path
from algorithms.nearest_neighbor import nearest_neighbor

ROOT = Path(__file__).resolve().parent
PARCELS_FILE = ROOT / "data" / "parcels.json"
GRAPH_FILE = ROOT / "data" / "delivery_graph.json"
CAPACITY_FILE = ROOT / "data" / "settings.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)


def load_parcels():
    return load_json(PARCELS_FILE)


def save_parcels(parcels):
    validate_parcels(parcels)
    save_json(PARCELS_FILE, parcels)


def load_network():
    return load_json(GRAPH_FILE)


def load_settings():
    return load_json(CAPACITY_FILE)


def validate_parcels(parcels):
    network = load_network()
    valid_destinations = set(network["graph"])
    seen = set()
    for p in parcels:
        required = {"parcel_id", "recipient", "destination", "weight_kg", "priority_score", "deadline"}
        missing = required - set(p)
        if missing:
            raise ValueError(f"Parcel is missing fields: {', '.join(sorted(missing))}")
        parcel_id = str(p["parcel_id"]).strip()
        if not parcel_id or parcel_id in seen:
            raise ValueError("Parcel IDs must be non-empty and unique.")
        seen.add(parcel_id)
        if p["destination"] not in valid_destinations or p["destination"] == "D0":
            raise ValueError(f"Invalid customer destination for {parcel_id}.")
        weight = int(p["weight_kg"])
        priority = int(p["priority_score"])
        if weight <= 0:
            raise ValueError(f"Weight for {parcel_id} must be positive.")
        if not 1 <= priority <= 10:
            raise ValueError(f"Priority for {parcel_id} must be between 1 and 10.")
        if len(str(p["deadline"])) != 10:
            raise ValueError(f"Deadline for {parcel_id} must use YYYY-MM-DD.")
    return True


def calculate_plan(parcels=None, capacity=None):
    parcels = load_parcels() if parcels is None else parcels
    settings = load_settings()
    capacity = int(settings["vehicle_capacity_kg"] if capacity is None else capacity)
    validate_parcels(parcels)

    sorted_parcels = prioritize_parcels(parcels)
    selected, total_weight, total_value = knapsack(sorted_parcels, capacity)

    network = load_network()
    graph = network["graph"]
    depot = network["depot"]
    selected_destinations = sorted({p["destination"] for p in selected})
    required_vertices = [depot] + selected_destinations

    distance_matrix = {}
    previous_maps = {}
    for source in required_vertices:
        distances, previous = dijkstra(graph, source)
        distance_matrix[source] = distances
        previous_maps[source] = previous

    # Keep only the locations that actually have selected parcels, plus depot.
    route, total_distance = nearest_neighbor(distance_matrix, depot)
    expanded_route = []
    leg_details = []
    for index in range(len(route) - 1):
        source, destination = route[index], route[index + 1]
        segment = reconstruct_path(previous_maps[source], source, destination)
        if not segment:
            raise ValueError(f"No path found from {source} to {destination}.")
        if not expanded_route:
            expanded_route.extend(segment)
        else:
            expanded_route.extend(segment[1:])
        leg_details.append({
            "from": source,
            "to": destination,
            "distance_km": distance_matrix[source][destination],
            "path": segment
        })

    return {
        "sorted_parcels": sorted_parcels,
        "selected_parcels": selected,
        "total_weight": total_weight,
        "total_value": total_value,
        "capacity": capacity,
        "remaining_capacity": capacity - total_weight,
        "selected_destinations": selected_destinations,
        "route": route,
        "expanded_route": expanded_route or [depot],
        "total_distance": total_distance,
        "legs": leg_details,
    }
