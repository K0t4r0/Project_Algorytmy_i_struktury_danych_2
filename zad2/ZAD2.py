import heapq
from collections import defaultdict

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
        return
    
    print(f"Dijkstra: the shortest way from {start} to {end}: {distances[end]}")

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
                return

    if distances[end] == float('inf'):
        print("Bellman-Ford-Moore: no path")
    else:
        print(f"Bellman-Ford-Moore: the shortest way from {start} to {end}: {distances[end]}")

def floyd_warshall(graph, n, start, end, w):
    INF = float('inf')
    dist = [[INF]*(n+1) for _ in range(n+1)]
    nxt = [[None]*(n+1) for _ in range(n+1)]

    for u in graph:
        for v, weight in graph[u].items():
            if weight < dist[u][v]:
                dist[u][v] = weight
                nxt[u][v] = v

    for k in range(1, n+1):
        for i in range(1, n+1):
            for j in range(1, n+1):
                if dist[i][k] != INF and dist[k][j] != INF and dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    for i in range(1, n+1):
        if dist[i][i] < 0:
            print("Floyd-Warshall: the graph contains a negative cycle")
            return
        
    print("Floyd-Warshall: ")

    for i in range(1, n+1):
        row = []
        for j in range(1, n+1):
            if dist[i][j] == INF:
                row.append("INF")
            else:
                row.append(str(dist[i][j]))
        print(" ".join(row))

    path = get_path(nxt, start, end)
    if path is None or dist[start][end] == INF:
        print("INF")
    else:
        print(dist[start][end], *path)

    cycle = get_path(nxt, w, w)
    if cycle is None or dist[w][w] == INF:
        print("INF")
    else:
        print(dist[w][w], *cycle)

def get_path(nxt, v, u):
    if nxt[v][u] is None:
        return None

    path = [v]
    curr = v
    while True:
        curr = nxt[curr][u]
        if curr is None:
            return None
        path.append(curr)
        if curr == u:
            break

    return path

# example
# 4 6
# 1 2 8
# 1 4 1
# 2 3 1
# 3 1 4
# 4 2 2 
# 4 3 9
# 2 4
# 2

hasNegative = False

n, m = map(int, input().split())

graph = defaultdict(dict)

for _ in range(m):
    w1, w2, g = map(int, input().split())
    
    if g < 0:
        hasNegative = True

    graph[w1][w2] = g

v, u = map(int, input().split())
w = int(input())

if hasNegative:
    print("Dijkstra: the graph contains negative weights")
else:
    dijkstra(graph, v, u, n)
moorea_bellmana(graph, n, v, u)
floyd_warshall(graph, n, v, u, w)