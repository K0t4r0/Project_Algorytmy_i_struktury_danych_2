import heapq
from collections import defaultdict

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    
    parents = {node: None for node in graph}
    
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                
    return distances, parents

def moorea_bellmana(graph, n, start, end):
    distances = {node: float('inf') for node in range(1, n + 1)}
    distances[start] = 0

    for _ in range(n - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                return "The graph contains a negative cycle"

    return distances[end]


# example
# 2 5 8 11
# 1 2 2
# 1 3 3
# 1 4 4
# 1 6 5
# 3 7 5 
# 3 5 7
# 4 5 6
# 4 8 1
# 4 6 2
# 5 7 3
# 5 8 2

start, end, n, m = map(int, input().split())

graph = defaultdict(dict)

for _ in range(m):
    w1, w2, g = map(int, input().split())
    
    graph[w1][w2] = g
    graph[w2][w1] = g

ways, parents = dijkstra(graph, start)

print(f"Dijkstra: The shortest way from {start} to {end}: {ways[end]}")

print(f"Algorytm Moore`a - Bellmana: The shortest way from {start} to {end}: {moorea_bellmana(graph, n, start, end)}")