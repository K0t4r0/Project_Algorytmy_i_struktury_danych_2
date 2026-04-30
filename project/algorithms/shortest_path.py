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
    
def bellman_ford(edges, n, start, end):
    dist = [float('inf')] * n
    parent = [-1] * n
    edge_from = [-1] * n
    dist[start] = 0
    
    for _ in range(n - 1):
        for i, (u, v, cap, cost, rev) in enumerate(edges):
            if cap > 0 and dist[u] != float('inf') and dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                parent[v] = u
                edge_from[v] = i

    for u, v, cap, cost, rev in edges:
        if cap > 0 and dist[u] != float('inf') and dist[u] + cost < dist[v]:
            # The graph contains a negative cycle
            return None
    
    return dist, parent, edge_from
