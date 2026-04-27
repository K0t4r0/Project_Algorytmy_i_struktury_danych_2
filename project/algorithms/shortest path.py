import heapq


def dijkstra(graph, start, end, n):
    distances = {node: float('inf') for node in range(1, n+1)}
    parents = {node: None for node in range(1, n+1)}
    
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    if distances[end] == float('inf'):
        print("Dijkstra: no path")
        return None
    return distances[end]
    


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
                print("Bellman-Ford-Moore: the graph contains a negative cycle")
                return None

    if distances[end] == float('inf'):
        print("Bellman-Ford-Moore: no path")
        return None
    else:
        return distances[end]
