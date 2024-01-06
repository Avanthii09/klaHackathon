import json
import networkx as nx
import matplotlib.pyplot as plt

input_file_path = '/21pw19/data1.json'
with open(input_file_path) as f:
    input_data = json.load(f)


def generate_delivery_paths(input_data):
    G = nx.Graph()

    # Adding nodes and edges to the graph based on neighborhood distances
    neighbourhoods_data = input_data["neighbourhoods"]
    for n_id, n_data in neighbourhoods_data.items():
        G.add_node(n_id, order_quantity=n_data["order_quantity"])

        for i, distance in enumerate(n_data["distances"]):
            if i > int(n_id[1:]):
                neighbor_id = f"n{i}"
                G.add_edge(n_id, neighbor_id, weight=distance)

    # Adding the restaurant node and edges
    restaurant_id = list(input_data["restaurants"].keys())[0]
    restaurant_distances = input_data["restaurants"][restaurant_id]["neighbourhood_distance"]
    for i, distance in enumerate(restaurant_distances):
        neighbor_id = f"n{i}"
        G.add_edge(restaurant_id, neighbor_id, weight=distance)

    start_node = restaurant_id
    nearest_neighbor_path = nearest_neighbor(G, start_node)

    # To Group the nodes by the delivery slots
    delivery_slots = group_nodes_by_capacity(nearest_neighbor_path, input_data["vehicles"]["v0"]["capacity"], restaurant_id)

    output = {"v0": {}}
    for i, slot in enumerate(delivery_slots):
        # Ensure each slot starts from the restaurant
        if slot[0] != restaurant_id:
            slot = [restaurant_id] + slot

        output["v0"][f"path{i + 1}"] = slot

        # Visualize the flow with capacity at each node
        visualize_delivery_flow(G, slot)

    with open("/21pw19/output1.json", "w") as output_file:
        json.dump(output, output_file, indent=2)


def nearest_neighbor(graph, start_node):
    visited_nodes = set([start_node])
    current_node = start_node
    path = [current_node]

    while len(visited_nodes) < len(graph.nodes):
        neighbors = [(neighbor, graph[current_node][neighbor]['weight']) for neighbor in graph.neighbors(current_node) if
                      neighbor not in visited_nodes]
        if not neighbors:
            break

        next_node = min(neighbors, key=lambda x: x[1])[0]
        path.append(next_node)
        visited_nodes.add(next_node)
        current_node = next_node

    return path


def group_nodes_by_capacity(path, capacity, restaurant_id):
    groups = []
    current_group = []
    current_capacity = 0

    for node in path:
        if node.startswith("n"):
            current_group.append(node)
            current_capacity += input_data["neighbourhoods"][node]["order_quantity"]

            if current_capacity >= capacity:
                groups.append(current_group)
                current_group = [restaurant_id]  # Start the next group with the restaurant
                current_capacity = 0

    if current_group:
        groups.append(current_group)

    return groups


def visualize_delivery_flow(graph, path):
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 6))

    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]

        # Draw edge with label
        nx.draw_networkx_edge_labels(graph, pos, edge_labels={(current_node, next_node): edge_labels[(current_node, next_node)]})

        # Draw node with order quantity
        nx.draw_networkx_nodes(graph, pos, nodelist=[current_node], node_size=700, node_color='b')
        nx.draw_networkx_nodes(graph, pos, nodelist=[next_node], node_size=700, node_color='r')

    # Draw final edge and node
    nx.draw_networkx_edges(graph, pos, edgelist=[(path[-2], path[-1])], edge_color='g')
    nx.draw_networkx_nodes(graph, pos, nodelist=[path[-1]], node_size=700, node_color='g')

    # Draw labels
    nx.draw_networkx_labels(graph, pos)

    # Show the plot
    plt.show()


generate_delivery_paths(input_data)
