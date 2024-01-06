import json
import networkx as nx
import matplotlib.pyplot as plt

# Read input data from the JSON file
input_file_path = '/21pw19/data1.json'
with open(input_file_path) as f:
    input_data = json.load(f)

# Create a graph
G = nx.Graph()

# Add nodes and edges to the graph based on neighborhood distances
neighbourhoods_data = input_data["neighbourhoods"]
for n_id, n_data in neighbourhoods_data.items():
    G.add_node(n_id)

    for i, distance in enumerate(n_data["distances"]):
        if i > int(n_id[1:]):
            neighbor_id = f"n{i}"
            G.add_edge(n_id, neighbor_id, weight=distance)

# Add the restaurant node and edges
restaurant_id = list(input_data["restaurants"].keys())[0]
restaurant_distances = input_data["restaurants"][restaurant_id]["neighbourhood_distance"]
for i, distance in enumerate(restaurant_distances):
    neighbor_id = f"n{i}"
    G.add_edge(restaurant_id, neighbor_id, weight=distance)

