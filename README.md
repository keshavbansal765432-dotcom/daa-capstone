# Mini-Courier Planner
### Design & Analysis of Algorithms (ETCCDA302) — Capstone

A Python/Tkinter desktop application implementing the assignment's integrated
courier-planning workflow:

- Merge Sort for parcel prioritization
- 0/1 Knapsack dynamic programming for vehicle loading
- Dijkstra shortest paths on a weighted adjacency-list graph
- Nearest Neighbor TSP approximation for a round-trip delivery sequence
- Runtime benchmarks and CSV output
- Parcel management GUI and sample JSON datasets

## Configuration
- Vehicle capacity: 100 kg
- Sample parcels: 20
- Locations: 5 including depot D0
- Starting/ending location: D0 (Courier Depot)

## Requirements
Python 3.9 or newer is recommended. The application uses only Python standard
library modules. On Linux, Tkinter may need to be installed separately.

### Fedora / Bazzite
If `python3 -m tkinter` fails, install the Tkinter package using the package
manager appropriate to your host/container. On Fedora-based systems this is
usually `python3-tkinter`.

### Ubuntu
`sudo apt install python3-tk`

## Run in VS Code
Open this folder in VS Code, then in its integrated terminal:

```bash
python3 --version
python3 -m tkinter
python3 main.py
```

## Run tests
From the project root:

```bash
python3 -m unittest discover -s tests -v
```

## Run benchmarks without opening the GUI

```bash
python3 performance/benchmark.py
```

The measured results are saved to `performance/results.csv`. Runtime varies by
computer and should be reported from actual runs, not copied from examples.

## GUI tabs
1. Dashboard — project configuration and algorithm workflow.
2. Parcel Management — add/delete parcels; changes persist in `data/parcels.json`.
3. Delivery Network — inspect locations and undirected road edges.
4. Route Planner — run the complete pipeline and inspect intermediate outputs.
5. Performance Analysis — benchmark algorithms and view a runtime chart.

## Data files
- `data/parcels.json`: parcel records.
- `data/delivery_graph.json`: location list and weighted adjacency list.
- `data/settings.json`: vehicle capacity and depot.

## Algorithm design
Merge Sort orders by descending priority score, then ascending deadline, then
parcel ID. Knapsack maximizes total priority score subject to integer kilogram
capacity. Dijkstra calculates shortest paths. The selected destination set is
passed to Nearest Neighbor using the shortest-path distance matrix. The tour is
expanded into the underlying road paths.

## Important academic notes
- The road distances are illustrative sample values, not live navigation data.
- Nearest Neighbor is a heuristic and does not guarantee the optimal TSP route.
- Knapsack uses priority score as parcel value; this is the model assumption.
- The benchmark records are measurements from the machine running the program.
- Understand the source code and be ready to trace algorithms in the viva.

## Suggested submission contents
Submit the complete project folder or GitHub repository, including source code,
tests, sample datasets, documentation, screenshots and actual benchmark CSV.
