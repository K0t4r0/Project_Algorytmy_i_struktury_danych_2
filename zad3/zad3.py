from collections import defaultdict, deque
import copy

#Zadanie 4
def dfs(u, sink, flow : float, visited : set, graph : dict) -> int:
    visited.add(u)

    if u == sink:
        return flow
    
    for v in graph[u]:
        capacity = graph[u][v]
        if v not in visited and capacity > 0:
            pushed = dfs(v, sink, min(flow, capacity), visited, graph)
            if pushed > 0:
                graph[u][v] -= pushed
                if u not in graph[v]: 
                    graph[v][u] = 0
                graph[v][u] += pushed
                
                return pushed
    return 0

def ford_fulkerson(graph : dict, source, sink) -> int:
    max_flow = 0
    
    while True:
        visited = set()
        pushed = dfs(source, sink, float('inf'), visited, graph)
        if pushed == 0:
            break
            
        max_flow += pushed
        
    return max_flow

#Zadanie 5
def bfs(source, sink, graph : dict):
    queue = deque([source])
    visited = set([source])
    parent = {}

    while queue:
        u = queue.popleft()

        for v in graph[u]:
            capacity = graph[u][v]
            if v not in visited and capacity > 0:
                queue.append(v)
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return parent
    return None
    
def edmonds_karp(graph, source, sink):
    max_flow = 0

    while True:
        parent = bfs(source, sink, graph)

        if parent is None:
            break

        path_flow = float('inf')

        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            
            graph[u][v] -= path_flow
            
            if u not in graph[v]:
                graph[v][u] = 0
                
            graph[v][u] += path_flow
            
            v = u

        max_flow += path_flow

    return max_flow


# Example
# 7 11
# s x 20
# s y 50
# y x 10
# x u 50
# x w 60
# y w 30
# w u 10
# w t 20
# u t 40
# u e 80
# e t 40

n, m = map(int, input().split())

siec = defaultdict(dict)

for _ in range(m):
    w1, w2, p = input().split()
    siec[w1][w2] = int(p)

siec_copy = copy.deepcopy(siec)

print(ford_fulkerson(siec, 's', 't'))
print(edmonds_karp(siec_copy, 's', 't'))