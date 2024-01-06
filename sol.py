import json
import networkx as nx
import matplotlib.pyplot as plt

# Reading input data from the JSON file
input_file_path = '/21pw19/data.json'
with open(input_file_path) as f:
    input_data = json.load(f)

def nearest_neighbor(graph, start_node):
    visited_nodes = set([start_node])
    current_node = start_node
    path = [current_node]

    while len(visited_nodes) < len(graph.nodes):
        neighbors = [(neighbor, graph[current_node][neighbor]['weight']) for neighbor in graph.neighbors(current_node) if neighbor not in visited_nodes]
        if not neighbors:
            break

        next_node = min(neighbors, key=lambda x: x[1])[0]
        path.append(next_node)
        visited_nodes.add(next_node)
        current_node = next_node

    return path

n_neighbourhoods = input_data["n_neighbourhoods"]
neighbourhoods_data = input_data["neighbourhoods"]
restaurant_id = list(input_data["restaurants"].keys())[0]
restaurant_distances = input_data["restaurants"][restaurant_id]["neighbourhood_distance"]


G=nx.Graph()

# Add nodes and edges to the graph based on neighborhood distances
for n_id, n_data in neighbourhoods_data.items():
    G.add_node(n_id)

    for i, distance in enumerate(n_data["distances"]):
        if i > int(n_id[1:]):  # Avoid duplicate edges since the distances are symmetric
            neighbor_id = f"n{i}"
            G.add_edge(n_id, neighbor_id, weight=distance)

# Add the restaurant node and edges
for i, distance in enumerate(restaurant_distances):
    neighbor_id = f"n{i}"
    G.add_edge(restaurant_id, neighbor_id, weight=distance)

# # Visualizing the graph using nx.draw_networkx
# pos = nx.spring_layout(G)
# nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_size=700)
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
# plt.show()


start_node = restaurant_id
nearest_neighbor_path = nearest_neighbor(G, start_node)

# Format the output
output = {"v0": {"path": nearest_neighbor_path}}

# Write the output to a file named "output0.json"
output_file_path = '/21pw19/output0.json'
with open(output_file_path, 'w') as output_file:
    json.dump(output, output_file, indent=2)

print(f"Output written to {output_file_path}")