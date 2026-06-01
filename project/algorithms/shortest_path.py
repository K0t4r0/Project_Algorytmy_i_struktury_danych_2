def bellman_ford(edges, n, start, end):
    dist = [float('inf')] * n
    parent = [-1] * n
    edge_from = [-1] * n
    dist[start] = 0
    
    for _ in range(n - 1):
        updated = False
        for i, (u, v, cap, cost, rev) in enumerate(edges):
            if cap > 0 and dist[u] != float('inf') and dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                parent[v] = u
                edge_from[v] = i
                updated = True
        if not updated:
            break

    for u, v, cap, cost, rev in edges:
        if cap > 0 and dist[u] != float('inf') and dist[u] + cost < dist[v]:
            # The graph contains a negative cycle
            return None
    
    return dist, parent, edge_from
