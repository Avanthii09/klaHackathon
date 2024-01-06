import json

def dijkstra(graph, start, end):
    unvisited = {node: float('inf') for node in graph}
    visited = {}
    current = start
    current_distance = 0
    unvisited[current] = current_distance

    while True:
        for neighbor, distance in graph[current]["distances"].items():
            if neighbor not in unvisited:
                continue
            new_distance = current_distance + distance
            if new_distance < unvisited[neighbor]:
                unvisited[neighbor] = new_distance

        visited[current] = current_distance
        del unvisited[current]
        if not unvisited:
            break
        current, current_distance = min(unvisited.items(), key=lambda x: x[1])

    return visited[end]

# Reading input data from the JSON file
input_file_path = '/21pw19/data.json'
with open(input_file_path) as f:
    input_data = json.load(f)

# Choose a specific neighborhood (e.g., "n0") and extract distances
neighborhood_id = "n0"
distances = input_data["neighbourhoods"][neighborhood_id]

# Finding the shortest path using Dijkstra's algorithm
start_node = "r0"
end_node = neighborhood_id
shortest_distance = dijkstra(input_data["neighbourhoods"], start_node, end_node)

# Print the output to the console
print(f"Shortest distance from {start_node} to {end_node}: {shortest_distance}")
