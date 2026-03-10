from collections import defaultdict


def dfs(u, target, flow : float, visited : set, graph : dict) -> int:
    visited.add(u)

    if u == target:
        return flow
    
    for v in graph[u]:
        capacity = graph[u][v]
        if v not in visited and capacity > 0:
            pushed = dfs(v, target, min(flow, capacity), visited, graph)
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

print(ford_fulkerson(siec, 's', 't'))