import pandas as pd
import random
import networkx as nx
from tqdm import tqdm

# -----------------------
# Define cities and systems
# -----------------------
cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
]

systems = [
    "Power Grid AI", "Internet Backbone AI", "Smart Water Utility",
    "Data Centers", "Hospitals", "Finance", "Logistics",
    "Public Transit", "Emergency Services", "Media", "Government Portals"
]

# -----------------------
# Define dependencies between systems
# -----------------------
dependencies = {
    "Power Grid AI": ["Internet Backbone AI", "Hospitals", "Data Centers", "Logistics"],
    "Internet Backbone AI": ["Data Centers", "Finance", "Media", "Government Portals"],
    "Smart Water Utility": ["Hospitals", "Public Transit"],
    "Data Centers": ["Finance", "Media"],
    "Hospitals": ["Emergency Services"],
    "Finance": ["Logistics"],
    "Public Transit": ["Emergency Services"],
    "Emergency Services": [],
    "Media": [],
    "Government Portals": []
}

# -----------------------
# Build graph template
# -----------------------
def build_graph():
    G = nx.DiGraph()
    for city in cities:
        for sys in systems:
            G.add_node((city, sys))
    for city in cities:
        for src, targets in dependencies.items():
            for tgt in targets:
                G.add_edge((city, src), (city, tgt))
    for i, city1 in enumerate(cities):
        for j, city2 in enumerate(cities):
            if i != j:
                for sys in ["Power Grid AI", "Internet Backbone AI", "Finance"]:
                    G.add_edge((city1, sys), (city2, sys))
    return G

# -----------------------
# Run 100 simulations
# -----------------------
all_records = []

for run in tqdm(range(1, 101), desc="Running simulations"):
    G = build_graph()

    # Start from a random city
    start_city = random.choice(cities)
    start_system = "Power Grid AI"
    start_node = (start_city, start_system)

    failure_time = {node: float('inf') for node in G.nodes}
    failure_time[start_node] = 0

    queue = [start_node]
    while queue:
        current = queue.pop(0)
        current_time = failure_time[current]
        for neighbor in G.successors(current):
            delay = random.randint(2, 15)
            proposed_time = current_time + delay
            if proposed_time < failure_time[neighbor]:
                failure_time[neighbor] = proposed_time
                queue.append(neighbor)

    for (city, system), f_time in failure_time.items():
        if f_time != float('inf'):
            all_records.append({
                "Run": run,
                "City": city,
                "System": system,
                "FailureTime": round(f_time, 1)
            })

# -----------------------
# Save all runs
# -----------------------
df = pd.DataFrame(all_records)
df.to_csv("failure_data_us.csv", index=False)

print(" 100-run failure_data_us.csv saved.")
