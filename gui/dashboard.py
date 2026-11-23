"""Tkinter desktop GUI for Mini-Courier Planner."""
import csv
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

from services import (
    load_parcels, save_parcels, load_network, load_settings,
    save_json, calculate_plan, PARCELS_FILE, ROOT
)
from algorithms.merge_sort import prioritize_parcels
from algorithms.knapsack import knapsack
from algorithms.dijkstra import dijkstra
from algorithms.nearest_neighbor import nearest_neighbor

PERFORMANCE_DIR = ROOT / "performance"


class CourierPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini-Courier Planner | DAA Capstone")
        self.geometry("1180x760")
        self.minsize(980, 650)
        self.configure(bg="#eef2f7")
        self.parcels = load_parcels()
        self.network = load_network()
        self.settings = load_settings()
        self._configure_style()
        self._build_header()
        self._build_tabs()
        self.refresh_all()

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#eef2f7")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("TLabel", background="#eef2f7", foreground="#172033", font=("Arial", 10))
        style.configure("Title.TLabel", font=("Arial", 21, "bold"), foreground="#ffffff", background="#14213d")
        style.configure("Subtitle.TLabel", font=("Arial", 10), foreground="#cbd5e1", background="#14213d")
        style.configure("CardTitle.TLabel", font=("Arial", 10, "bold"), background="#ffffff", foreground="#64748b")
        style.configure("Metric.TLabel", font=("Arial", 23, "bold"), background="#ffffff", foreground="#14213d")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=8)
        style.configure("Accent.TButton", background="#2563eb", foreground="white")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("Treeview", rowheight=27, font=("Arial", 9), background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        style.configure("TNotebook", background="#eef2f7", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(15, 9), font=("Arial", 10, "bold"))

    def _build_header(self):
        header = tk.Frame(self, bg="#14213d", height=88)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="MINI-COURIER PLANNER", bg="#14213d", fg="white",
                 font=("Arial", 21, "bold")).pack(anchor="w", padx=24, pady=(15, 2))
        tk.Label(header, text="Design & Analysis of Algorithms | Sorting • Dynamic Programming • Graphs",
                 bg="#14213d", fg="#cbd5e1", font=("Arial", 10)).pack(anchor="w", padx=25)

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=16)
        self.dashboard_tab = ttk.Frame(self.notebook, padding=16)
        self.parcels_tab = ttk.Frame(self.notebook, padding=16)
        self.network_tab = ttk.Frame(self.notebook, padding=16)
        self.planner_tab = ttk.Frame(self.notebook, padding=16)
        self.performance_tab = ttk.Frame(self.notebook, padding=16)
        for tab, title in [
            (self.dashboard_tab, "Dashboard"),
            (self.parcels_tab, "Parcel Management"),
            (self.network_tab, "Delivery Network"),
            (self.planner_tab, "Route Planner"),
            (self.performance_tab, "Performance Analysis")
        ]:
            self.notebook.add(tab, text=title)
        self._build_dashboard()
        self._build_parcels()
        self._build_network()
        self._build_planner()
        self._build_performance()

    def _metric_card(self, parent, title, variable):
        card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=variable, style="Metric.TLabel").pack(anchor="w", pady=(7, 0))
        return card

    def _build_dashboard(self):
        ttk.Label(self.dashboard_tab, text="Operations overview", font=("Arial", 17, "bold")).pack(anchor="w", pady=(0, 12))
        cards = ttk.Frame(self.dashboard_tab)
        cards.pack(fill="x")
        self.metric_parcels = tk.StringVar(value="0")
        self.metric_weight = tk.StringVar(value="0 kg")
        self.metric_capacity = tk.StringVar(value="100 kg")
        self.metric_locations = tk.StringVar(value="5")
        for title, var in [
            ("TOTAL PARCELS", self.metric_parcels),
            ("TOTAL PARCEL WEIGHT", self.metric_weight),
            ("VEHICLE CAPACITY", self.metric_capacity),
            ("DELIVERY LOCATIONS", self.metric_locations)
        ]:
            self._metric_card(cards, title, var).pack(side="left", fill="both", expand=True, padx=(0, 10))
        ttk.Label(self.dashboard_tab, text="System workflow", font=("Arial", 14, "bold")).pack(anchor="w", pady=(28, 10))
        workflow = [
            ("01", "Merge Sort", "Prioritize parcels by priority score and deadline"),
            ("02", "0/1 Knapsack", "Choose the highest-value parcel combination within capacity"),
            ("03", "Dijkstra", "Calculate shortest road paths between required locations"),
            ("04", "Nearest Neighbor TSP", "Build an approximate round-trip delivery sequence"),
            ("05", "Performance", "Measure and compare algorithm execution times")
        ]
        for number, name, description in workflow:
            row = ttk.Frame(self.dashboard_tab, style="Card.TFrame", padding=10)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=number, bg="#dbeafe", fg="#1d4ed8", font=("Arial", 11, "bold"), width=4, pady=5).pack(side="left", padx=(0, 12))
            text_frame = tk.Frame(row, bg="white")
            text_frame.pack(side="left", fill="x", expand=True)
            tk.Label(text_frame, text=name, bg="white", fg="#14213d", font=("Arial", 10, "bold")).pack(anchor="w")
            tk.Label(text_frame, text=description, bg="white", fg="#64748b", font=("Arial", 9)).pack(anchor="w")

    def _build_parcels(self):
        ttk.Label(self.parcels_tab, text="Parcel management", font=("Arial", 17, "bold")).pack(anchor="w")
        ttk.Label(self.parcels_tab, text="Add and remove sample parcels. Data is saved in data/parcels.json.",
                  foreground="#64748b").pack(anchor="w", pady=(2, 12))
        form = ttk.LabelFrame(self.parcels_tab, text="Add a parcel", padding=10)
        form.pack(fill="x", pady=(0, 12))
        self.form_vars = {key: tk.StringVar() for key in ["parcel_id", "recipient", "destination", "weight_kg", "priority_score", "deadline"]}
        fields = [
            ("Parcel ID", "parcel_id", 12), ("Recipient", "recipient", 14),
            ("Destination", "destination", 9), ("Weight kg", "weight_kg", 8),
            ("Priority 1-10", "priority_score", 9), ("Deadline YYYY-MM-DD", "deadline", 13)
        ]
        for index, (label, key, width) in enumerate(fields):
            cell = ttk.Frame(form)
            cell.grid(row=0, column=index, padx=4, sticky="w")
            ttk.Label(cell, text=label).pack(anchor="w")
            if key == "destination":
                widget = ttk.Combobox(cell, textvariable=self.form_vars[key], values=["L1", "L2", "L3", "L4"], width=width-2, state="readonly")
            else:
                widget = ttk.Entry(cell, textvariable=self.form_vars[key], width=width)
            widget.pack()
        ttk.Button(form, text="Add Parcel", style="Accent.TButton", command=self.add_parcel).grid(row=0, column=len(fields), padx=8, pady=(16, 0))
        table_frame = ttk.Frame(self.parcels_tab)
        table_frame.pack(fill="both", expand=True)
        columns = ("parcel_id", "recipient", "destination", "weight_kg", "priority_score", "deadline")
        self.parcel_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
        headings = ["Parcel ID", "Recipient", "Destination", "Weight (kg)", "Priority", "Deadline"]
        widths = [100, 150, 110, 110, 100, 130]
        for col, heading, width in zip(columns, headings, widths):
            self.parcel_tree.heading(col, text=heading)
            self.parcel_tree.column(col, width=width, anchor="center")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.parcel_tree.yview)
        self.parcel_tree.configure(yscrollcommand=scroll.set)
        self.parcel_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        ttk.Button(self.parcels_tab, text="Delete Selected Parcel", command=self.delete_parcel).pack(anchor="e", pady=10)

    def _build_network(self):
        ttk.Label(self.network_tab, text="Delivery network", font=("Arial", 17, "bold")).pack(anchor="w")
        ttk.Label(self.network_tab, text="Undirected weighted graph. Edge weights represent illustrative road distances in kilometres.",
                  foreground="#64748b").pack(anchor="w", pady=(2, 12))
        location_frame = ttk.LabelFrame(self.network_tab, text="Locations", padding=10)
        location_frame.pack(fill="x", pady=(0, 12))
        for loc in self.network["locations"]:
            ttk.Label(location_frame, text=f'{loc["id"]}  —  {loc["name"]}').pack(anchor="w", pady=2)
        edge_frame = ttk.LabelFrame(self.network_tab, text="Road connections", padding=10)
        edge_frame.pack(fill="both", expand=True)
        self.edge_tree = ttk.Treeview(edge_frame, columns=("from", "to", "distance"), show="headings", height=12)
        for col, title, width in [("from", "From", 160), ("to", "To", 160), ("distance", "Distance (km)", 180)]:
            self.edge_tree.heading(col, text=title)
            self.edge_tree.column(col, width=width, anchor="center")
        self.edge_tree.pack(fill="both", expand=True)
        seen = set()
        for source, neighbors in self.network["graph"].items():
            for destination, distance in neighbors:
                edge = tuple(sorted((source, destination)))
                if edge not in seen:
                    seen.add(edge)
                    self.edge_tree.insert("", "end", values=(source, destination, distance))
        ttk.Label(self.network_tab, text="Note: these are sample distances for algorithm demonstration, not live navigation data.",
                  foreground="#b45309").pack(anchor="w", pady=8)

    def _build_planner(self):
        ttk.Label(self.planner_tab, text="Courier route planner", font=("Arial", 17, "bold")).pack(anchor="w")
        ttk.Label(self.planner_tab, text="Run the integrated algorithm pipeline using the current parcel list and vehicle capacity.",
                  foreground="#64748b").pack(anchor="w", pady=(2, 12))
        controls = ttk.Frame(self.planner_tab)
        controls.pack(fill="x")
        ttk.Label(controls, text="Vehicle capacity (kg):").pack(side="left")
        self.capacity_var = tk.StringVar(value=str(self.settings["vehicle_capacity_kg"]))
        ttk.Entry(controls, textvariable=self.capacity_var, width=8).pack(side="left", padx=8)
        ttk.Button(controls, text="Generate Delivery Plan", style="Accent.TButton", command=self.run_planner).pack(side="left", padx=8)
        self.plan_text = tk.Text(self.planner_tab, wrap="word", font=("Consolas", 10), bg="#ffffff", fg="#172033",
                                 relief="flat", padx=12, pady=12)
        self.plan_text.pack(fill="both", expand=True, pady=14)
        self.plan_text.insert("1.0", "Click 'Generate Delivery Plan' to run Merge Sort, 0/1 Knapsack, Dijkstra and Nearest Neighbor TSP.")
        self.plan_text.configure(state="disabled")

    def _build_performance(self):
        ttk.Label(self.performance_tab, text="Performance analysis", font=("Arial", 17, "bold")).pack(anchor="w")
        ttk.Label(self.performance_tab, text="Run repeatable sample benchmarks and save measured runtimes to performance/results.csv.",
                  foreground="#64748b").pack(anchor="w", pady=(2, 12))
        ttk.Button(self.performance_tab, text="Run Benchmarks", style="Accent.TButton", command=self.run_benchmarks).pack(anchor="w")
        self.benchmark_status = tk.StringVar(value="No benchmark has been run in this session.")
        ttk.Label(self.performance_tab, textvariable=self.benchmark_status).pack(anchor="w", pady=8)
        self.chart = tk.Canvas(self.performance_tab, bg="white", height=300, highlightthickness=0)
        self.chart.pack(fill="both", expand=True, pady=8)
        self.results_tree = ttk.Treeview(self.performance_tab, columns=("algorithm", "size", "time"), show="headings", height=7)
        for col, title, width in [("algorithm", "Algorithm", 250), ("size", "Input size", 150), ("time", "Time (seconds)", 200)]:
            self.results_tree.heading(col, text=title)
            self.results_tree.column(col, width=width, anchor="center")
        self.results_tree.pack(fill="x")

    def refresh_all(self):
        self.parcels = load_parcels()
        self.metric_parcels.set(str(len(self.parcels)))
        self.metric_weight.set(f'{sum(int(p["weight_kg"]) for p in self.parcels)} kg')
        self.metric_capacity.set(f'{self.settings["vehicle_capacity_kg"]} kg')
        self.metric_locations.set(str(len(self.network["locations"])))
        for item in self.parcel_tree.get_children():
            self.parcel_tree.delete(item)
        for p in self.parcels:
            self.parcel_tree.insert("", "end", values=(
                p["parcel_id"], p["recipient"], p["destination"],
                p["weight_kg"], p["priority_score"], p["deadline"]
            ))

    def add_parcel(self):
        try:
            p = {
                "parcel_id": self.form_vars["parcel_id"].get().strip(),
                "recipient": self.form_vars["recipient"].get().strip(),
                "destination": self.form_vars["destination"].get().strip(),
                "weight_kg": int(self.form_vars["weight_kg"].get()),
                "priority_score": int(self.form_vars["priority_score"].get()),
                "deadline": self.form_vars["deadline"].get().strip()
            }
            updated = self.parcels + [p]
            save_parcels(updated)
            for var in self.form_vars.values():
                var.set("")
            self.refresh_all()
            messagebox.showinfo("Parcel added", f'Parcel {p["parcel_id"]} was saved.')
        except Exception as exc:
            messagebox.showerror("Cannot add parcel", str(exc))

    def delete_parcel(self):
        selection = self.parcel_tree.selection()
        if not selection:
            messagebox.showwarning("Select a parcel", "Select a parcel row first.")
            return
        parcel_id = self.parcel_tree.item(selection[0], "values")[0]
        if not messagebox.askyesno("Confirm deletion", f"Delete parcel {parcel_id}?"):
            return
        self.parcels = [p for p in self.parcels if p["parcel_id"] != parcel_id]
        save_parcels(self.parcels)
        self.refresh_all()

    def run_planner(self):
        try:
            capacity = int(self.capacity_var.get())
            if capacity < 0:
                raise ValueError("Capacity cannot be negative.")
            save_json(ROOT / "data" / "settings.json", {"vehicle_capacity_kg": capacity, "depot": "D0"})
            self.settings = load_settings()
            result = calculate_plan(self.parcels, capacity)
            lines = []
            lines.append("MINI-COURIER PLANNER — GENERATED DELIVERY PLAN")
            lines.append("=" * 58)
            lines.append(f'Vehicle capacity: {capacity} kg')
            lines.append(f'Total input parcels: {len(self.parcels)}')
            lines.append(f'Total input parcel weight: {sum(int(p["weight_kg"]) for p in self.parcels)} kg')
            lines.append("")
            lines.append("1. MERGE SORT — PRIORITIZED PARCELS")
            lines.append("-" * 58)
            for p in result["sorted_parcels"]:
                lines.append(f'{p["parcel_id"]} | priority {p["priority_score"]} | deadline {p["deadline"]} | {p["weight_kg"]} kg')
            lines.append("")
            lines.append("2. 0/1 KNAPSACK — SELECTED PARCELS")
            lines.append("-" * 58)
            for p in result["selected_parcels"]:
                lines.append(f'{p["parcel_id"]} | {p["recipient"]} | {p["destination"]} | {p["weight_kg"]} kg | value {p["priority_score"]}')
            lines.append(f'Total selected weight: {result["total_weight"]} kg')
            lines.append(f'Total priority value: {result["total_value"]}')
            lines.append(f'Remaining capacity: {result["remaining_capacity"]} kg')
            lines.append("")
            lines.append("3. DIJKSTRA + NEAREST NEIGHBOR — ROUTE")
            lines.append("-" * 58)
            lines.append("Selected delivery locations: " + (", ".join(result["selected_destinations"]) or "None"))
            lines.append("Visit sequence: " + " -> ".join(result["route"]))
            lines.append("Road-by-road shortest paths:")
            for leg in result["legs"]:
                lines.append(f'  {leg["from"]} -> {leg["to"]}: {" -> ".join(leg["path"])} ({leg["distance_km"]} km)')
            lines.append("Expanded road route: " + " -> ".join(result["expanded_route"]))
            lines.append(f'Total round-trip distance: {result["total_distance"]} km')
            lines.append("")
            lines.append("Method note: Nearest Neighbor is a heuristic and does not guarantee the globally optimal TSP tour.")
            self.plan_text.configure(state="normal")
            self.plan_text.delete("1.0", "end")
            self.plan_text.insert("1.0", "\n".join(lines))
            self.plan_text.configure(state="disabled")
        except Exception as exc:
            messagebox.showerror("Planning error", str(exc))

    def run_benchmarks(self):
        try:
            PERFORMANCE_DIR.mkdir(parents=True, exist_ok=True)
            rows = []
            rng = random.Random(42)

            for size in (20, 100, 500, 1000):
                sample = [
                    {"parcel_id": f"S{i:04d}", "priority_score": rng.randint(1, 10),
                     "deadline": f"2026-12-{rng.randint(1, 28):02d}"}
                    for i in range(size)
                ]
                start = time.perf_counter()
                prioritize_parcels(sample)
                elapsed = time.perf_counter() - start
                rows.append(("Merge Sort", size, elapsed))

            for size in (10, 20, 40, 80):
                sample = [
                    {"parcel_id": f"K{i:04d}", "weight_kg": rng.randint(1, 20),
                     "priority_score": rng.randint(1, 10)}
                    for i in range(size)
                ]
                start = time.perf_counter()
                knapsack(sample, 100)
                elapsed = time.perf_counter() - start
                rows.append(("0/1 Knapsack", size, elapsed))

            graph = self.network["graph"]
            for source in graph:
                start = time.perf_counter()
                dijkstra(graph, source)
                elapsed = time.perf_counter() - start
                rows.append(("Dijkstra", len(graph), elapsed))

            for size in (5, 10, 20, 40):
                nodes = [f"N{i}" for i in range(size)]
                matrix = {
                    a: {b: (0 if a == b else abs(i-j) + ((i+j) % 5) + 1)
                        for j, b in enumerate(nodes)}
                    for i, a in enumerate(nodes)
                }
                start = time.perf_counter()
                nearest_neighbor(matrix, nodes[0])
                elapsed = time.perf_counter() - start
                rows.append(("Nearest Neighbor", size, elapsed))

            output = PERFORMANCE_DIR / "results.csv"
            with output.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["algorithm", "input_size", "runtime_seconds"])
                writer.writerows(rows)

            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            for algorithm, size, elapsed in rows:
                self.results_tree.insert("", "end", values=(algorithm, size, f"{elapsed:.8f}"))

            self.benchmark_status.set(f"Completed {len(rows)} benchmark measurements. Saved: {output.relative_to(ROOT)}")
            self.draw_chart(rows)
        except Exception as exc:
            messagebox.showerror("Benchmark error", str(exc))

    def draw_chart(self, rows):
        self.chart.delete("all")
        width = max(self.chart.winfo_width(), 700)
        height = max(self.chart.winfo_height(), 280)
        self.chart.create_text(20, 18, anchor="w", text="Measured runtime by algorithm (seconds)",
                               font=("Arial", 11, "bold"), fill="#172033")
        grouped = {}
        for name, size, elapsed in rows:
            grouped.setdefault(name, []).append((size, elapsed))
        names = list(grouped)
        chart_top, chart_bottom = 55, height - 35
        max_value = max((t for values in grouped.values() for _, t in values), default=1) or 1
        row_height = max(32, (chart_bottom - chart_top) / max(1, len(names)))
        for index, name in enumerate(names):
            y = chart_top + index * row_height
            maximum = max(t for _, t in grouped[name])
            bar_width = (width - 300) * maximum / max_value
            self.chart.create_text(20, y + 10, anchor="w", text=name, fill="#334155", font=("Arial", 9, "bold"))
            self.chart.create_rectangle(190, y, 190 + bar_width, y + 20, fill="#3b82f6", outline="")
            self.chart.create_text(200 + bar_width, y + 10, anchor="w",
                                   text=f"{maximum:.6f}s", fill="#475569", font=("Arial", 8))


if __name__ == "__main__":
    CourierPlannerApp().mainloop()
