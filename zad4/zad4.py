from collections import defaultdict, deque

def bfs(graph, start, end):
    levels = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v, cap in graph[u].items():
            if cap > 0 and v not in levels:
                levels[v] = levels[u] + 1
                queue.append(v)
    return levels if end in levels else None

def dfs(graph, levels, u, end, flow):
    if u == end or flow == 0:
        return flow
    
    for v, cap in graph[u].items():
        if levels.get(v) == levels[u] + 1 and cap > 0:
            pushed = dfs(graph, levels, v, end, min(flow, cap))
            if pushed > 0:
                graph[u][v] -= pushed
                if u not in graph[v]: graph[v][u] = 0
                graph[v][u] += pushed
                return pushed
    return 0

def dinica(graph, start, end):
    max_flow = 0
    while True:
        levels = bfs(graph, start, end)
        if not levels:
            break
        
        while True:
            pushed = dfs(graph, levels, start, end, float('inf'))
            if pushed == 0:
                break
            max_flow += pushed
            
    print(f"max_flow: {max_flow}")


# Example
# 5 7
# s x 18
# s y 20
# x y 15
# x u 20
# y u 12
# y t 17
# u t 14 

line = input().split()
n, m = map(int, line)
graph = defaultdict(dict)

for _ in range(m):
    u, v, p = input().split()
    p = int(p)
    graph[u][v] = p
    if u not in graph[v]: 
        graph[v][u] = 0

dinica(graph, "s", "t")