# import json
# import networkx as nx

# input_file_path = '/21pw19/data1.json'
# with open(input_file_path) as f:
#     input_data = json.load(f)


# def generate_delivery_paths(input_data):
#     G = nx.Graph()

#     # Adding nodes and edges to the graph based on neighborhood distances
#     neighbourhoods_data = input_data["neighbourhoods"]
#     for n_id, n_data in neighbourhoods_data.items():
#         G.add_node(n_id)

#         for i, distance in enumerate(n_data["distances"]):
#             if i > int(n_id[1:]):
#                 neighbor_id = f"n{i}"
#                 G.add_edge(n_id, neighbor_id, weight=distance)

#     # Adding the restaurant node and edges
#     restaurant_id = list(input_data["restaurants"].keys())[0]
#     restaurant_distances = input_data["restaurants"][restaurant_id]["neighbourhood_distance"]
#     for i, distance in enumerate(restaurant_distances):
#         neighbor_id = f"n{i}"
#         G.add_edge(restaurant_id, neighbor_id, weight=distance)

#     start_node = restaurant_id
#     nearest_neighbor_path = nearest_neighbor(G, start_node)

#     # To Group the nodes by the delivery slots
#     delivery_slots = group_nodes_by_capacity(nearest_neighbor_path, input_data["vehicles"]["v0"]["capacity"])

#     output = {"v0": {}}
#     for i, slot in enumerate(delivery_slots):
#         output["v0"][f"path{i + 1}"] = slot

#     with open("/21pw19/output1.json", "w") as output_file:
#         json.dump(output, output_file, indent=2)

# def nearest_neighbor(graph, start_node):
#     visited_nodes = set([start_node])
#     current_node = start_node
#     path = [current_node]

#     while len(visited_nodes) < len(graph.nodes):
#         neighbors = [(neighbor, graph[current_node][neighbor]['weight']) for neighbor in graph.neighbors(current_node) if neighbor not in visited_nodes]
#         if not neighbors:
#             break

#         next_node = min(neighbors, key=lambda x: x[1])[0]
#         path.append(next_node)
#         visited_nodes.add(next_node)
#         current_node = next_node

#     return path

# def group_nodes_by_capacity(path, capacity):
#     groups = []
#     current_group = []
#     current_capacity = 0

#     for node in path:
#         if node.startswith("n"):
#             current_group.append(node)
#             current_capacity += input_data["neighbourhoods"][node]["order_quantity"]

#             if current_capacity >= capacity:
#                 groups.append(current_group)
#                 current_group = []
#                 current_capacity = 0

#     if current_group:
#         groups.append(current_group)

#     return groups

# generate_delivery_paths(input_data)


import json
import networkx as nx
import itertools

def generate_delivery_paths(input_data):
    G = nx.Graph()

    # Adding nodes and edges to the graph based on neighborhood distances
    neighbourhoods_data = input_data["neighbourhoods"]
    for n_id, n_data in neighbourhoods_data.items():
        G.add_node(n_id)

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
    all_neighbourhoods = list(neighbourhoods_data.keys())
    if restaurant_id in all_neighbourhoods:
        all_neighbourhoods.remove(restaurant_id)

    # Find the optimal paths with capacity constraint
    optimal_paths = find_optimal_paths(
        G, start_node, all_neighbourhoods, input_data["vehicles"]["v0"]["capacity"])

    output = {"v0": {}}
    for i, path in enumerate(optimal_paths):
        # Ensure each path starts and ends at the restaurant
        path = [restaurant_id] + path + [restaurant_id]
        output["v0"][f"path{i + 1}"] = path

    with open("/21pw19/output1.json", "w") as output_file:
        json.dump(output, output_file, indent=2)



def find_optimal_paths(graph, start_node, neighbourhoods, capacity):
    optimal_paths = []

    # Generate all possible permutations of neighbourhood nodes
    permutations = list(itertools.permutations(neighbourhoods))

    for perm in permutations:
        current_path = list(perm)
        current_capacity = 0
        current_distance = 0
        paths = []

        for node in current_path:
            # Calculate distance and check capacity
            distance_to_node = graph[start_node][node]['weight']
            if current_capacity + input_data["neighbourhoods"][node]["order_quantity"] <= capacity:
                current_distance += distance_to_node
                current_capacity += input_data["neighbourhoods"][node]["order_quantity"]
                paths.append(node)
            else:
                break  # Stop adding nodes to this path if capacity is exceeded

        if paths:
            optimal_paths.append(paths)

    return optimal_paths

if __name__ == "__main__":
    input_file_path = '/21pw19/data1.json'
    with open(input_file_path) as f:
        input_data = json.load(f)

    generate_delivery_paths(input_data)
