import heapq
from collections import defaultdict

def dijkstra(graph, start, end):
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
                
    # return distances, parents
    list_rev = []
    current_node = end

    while not bool(list_rev) or list_rev[-1] != start:
        list_rev.append(current_node)
        current_node = parents[current_node]

    print("Dijkstra: The shortest way: ", end="")
    while bool(list_rev):
        print(list_rev[-1], end="")
        list_rev.pop()
        if bool(list_rev):
            print(" -> ", end="")
    print("\nTotal weight of the shortest route:", distances[end])

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

    print(f"Bellman-Ford-Moore: the shortest way from {start} to {end}: {distances[end]}")


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

dijkstra(graph, start, end)
moorea_bellmana(graph, n, start, end)