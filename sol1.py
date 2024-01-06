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



# from itertools import permutations
# import json
# import networkx as nx
# from networkx.algorithms.approximation import traveling_salesman_problem

# def read_input_data(input_file_path):
#     with open(input_file_path) as f:
#         input_data = json.load(f)
#     return input_data

# def construct_graph(neighbourhoods_data, restaurant_id, restaurant_distances):
#     G = nx.Graph()

#     # Adding nodes and edges to the graph based on neighborhood distances
#     for n_id, n_data in neighbourhoods_data.items():
#         G.add_node(n_id)
#         for i, distance in enumerate(n_data["distances"]):
#             if i > int(n_id[1:]):
#                 neighbor_id = f"n{i}"
#                 G.add_edge(n_id, neighbor_id, weight=distance)

#     # Adding the restaurant node and edges
#     for i, distance in enumerate(restaurant_distances):
#         neighbor_id = f"n{i}"
#         G.add_edge(restaurant_id, neighbor_id, weight=distance)

#     return G

# def assign_orders_to_slots(path, orders):
#     current_capacity = 0  # Initialize current_capacity
#     slot = []
#     for node in path[1:-1]:
#         order = orders.get(node, {"order_quantity": 0})  # Use .get() to handle missing keys
#         if current_capacity + order['order_quantity'] <= vehicle_capacity:
#             slot.append(node)
#             current_capacity += order['order_quantity']
#     return [restaurant_id] + slot + [restaurant_id]



# # Reading input data
# input_file_path = '/21pw19/data1.json'
# input_data = read_input_data(input_file_path)

# # Extracting data from input
# n_neighbourhoods = input_data["n_neighbourhoods"]
# neighbourhoods_data = input_data["neighbourhoods"]
# restaurant_id = list(input_data["restaurants"].keys())[0]
# restaurant_distances = input_data["restaurants"][restaurant_id]["neighbourhood_distance"]
# vehicle_capacity = input_data["vehicles"]["v0"]["capacity"]

# # Constructing the graph
# G = construct_graph(neighbourhoods_data, restaurant_id, restaurant_distances)

# # Creating distance matrix
# distance_matrix = nx.floyd_warshall_numpy(G, weight='weight')

# # Solving TSP to find an optimal path
# tsp_path = traveling_salesman_problem(G, cycle=False, weight='weight')


# # Assigning orders to slots
# orders = {}
# for node in tsp_path:
#     if node != restaurant_id:
#         orders[node] = {"order_quantity": neighbourhoods_data[node]["order_quantity"]}

# # Creating delivery paths
# delivery_paths = [tsp_path]

# # Assigning orders to slots
# slots = {"path1": assign_orders_to_slots(tsp_path, orders)}



# # Writing output data
# output_file_path = '/21pw19/output1.json'
# with open(output_file_path, 'w') as output_file:
#     json.dump({"v0": slots}, output_file, indent=2)

# print(f"Output written to {output_file_path}")





import json
import networkx as nx

def read_input_data(input_file_path):
    with open(input_file_path) as f:
        input_data = json.load(f)
    return input_data

def construct_graph(neighbourhoods_data, restaurant_id, restaurant_distances):
    G = nx.Graph()

    # Adding nodes and edges to the graph based on neighborhood distances
    for n_id, n_data in neighbourhoods_data.items():
        G.add_node(n_id)
        for i, distance in enumerate(n_data["distances"]):
            if i > int(n_id[1:]):
                neighbor_id = f"n{i}"
                G.add_edge(n_id, neighbor_id, weight=distance)

    # Adding the restaurant node and edges
    for i, distance in enumerate(restaurant_distances):
        neighbor_id = f"n{i}"
        G.add_edge(restaurant_id, neighbor_id, weight=distance)

    return G

def nearest_neighbor(graph, start_node):
    visited_nodes = set([start_node])
    current_node = start_node
    path = [current_node]

    while set(graph.nodes) - visited_nodes:
        neighbors = [(neighbor, graph[current_node][neighbor]['weight']) for neighbor in graph.neighbors(current_node) if neighbor not in visited_nodes]
        if not neighbors:
            break

        next_node = min(neighbors, key=lambda x: x[1])[0]
        path.append(next_node)
        visited_nodes.add(next_node)
        current_node = next_node

    return path


def generate_paths(graph, start_node, vehicle_capacity, orders):
    all_paths = []
    remaining_nodes = set(graph.nodes) - {start_node}

    while remaining_nodes:
        path = nearest_neighbor(graph, start_node)
        current_capacity = 0
        new_path = [start_node]

        for node in path[1:]:
            order = orders[node]
            if current_capacity + order['order_quantity'] <= vehicle_capacity:
                new_path.append(node)
                current_capacity += order['order_quantity']
            else:
                all_paths.append(new_path + [start_node])
                remaining_nodes -= set(new_path)
                new_path = [start_node]
                current_capacity = 0

        if new_path != [start_node]:
            all_paths.append(new_path)
            remaining_nodes -= set(new_path)

    return all_paths

def assign_orders_to_slots(paths, orders):
    slots = {}
    for i, path in enumerate(paths):
        slot = []
        current_capacity = 0
        for node in path[1:-1]:
            order = orders[node]
            if current_capacity + order['order_quantity'] <= vehicle_capacity:
                slot.append(node)
                current_capacity += order['order_quantity']
        slots[f"path{i + 1}"] = [restaurant_id] + slot + [restaurant_id]
    return slots

# Reading input data
input_file_path = '/21pw19/data1.json'
input_data = read_input_data(input_file_path)

# Extracting data from input
neighbourhoods_data = input_data["neighbourhoods"]
restaurant_id = list(input_data["restaurants"].keys())[0]
restaurant_distances = input_data["restaurants"][restaurant_id]["neighbourhood_distance"]
vehicle_capacity = input_data["vehicles"]["v0"]["capacity"]

# Constructing the graph
G = construct_graph(neighbourhoods_data, restaurant_id, restaurant_distances)

# Assigning orders to slots
orders = {node: {"order_quantity": neighbourhoods_data[node]["order_quantity"]} for node in G.nodes if node != restaurant_id}

all_paths = generate_paths(G, restaurant_id, vehicle_capacity, orders)

# Print paths for debugging
for i, path in enumerate(all_paths):
    print(f"path{i + 1} cost : ", sum(G[path[j]][path[j + 1]]['weight'] for j in range(len(path) - 1)))
    print(path)

# Check if all neighborhoods are visited
visited_neighborhoods = set(node for path in all_paths for node in path)
all_neighborhoods = set(neighbourhoods_data.keys())
remaining_neighborhoods = all_neighborhoods - visited_neighborhoods

if remaining_neighborhoods:
    print("Validation failed. Unvisited neighborhoods:", remaining_neighborhoods)
else:
    print("Validation passed. All neighborhoods visited.")

# Writing output data
output_file_path = '/21pw19/output1.json'
with open(output_file_path, 'w') as output_file:
    json.dump({"v0": assign_orders_to_slots(all_paths, orders)}, output_file, indent=2)

print(f"Output written to {output_file_path}")