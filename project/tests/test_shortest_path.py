from algorithms.shortest_path import bellman_ford


def test_bellman_ford_returns_distance_parent_and_edge_info():
    edges = [
        (0, 1, 1, 4, 0),
        (0, 2, 1, 2, 0),
        (2, 1, 1, 1, 0),
    ]

    dist, parent, edge_from = bellman_ford(edges, 3, 0, 1)

    assert dist[1] == 3
    assert parent[1] == 2
    assert edge_from[1] == 2


def test_bellman_ford_ignores_edges_without_capacity():
    edges = [
        (0, 1, 0, 1, 0),
        (0, 2, 1, 5, 0),
        (2, 1, 1, 5, 0),
    ]

    dist, parent, edge_from = bellman_ford(edges, 3, 0, 1)

    assert dist[1] == 10
    assert parent[1] == 2


def test_bellman_ford_returns_none_for_negative_cycle():
    edges = [
        (0, 1, 1, 1, 0),
        (1, 2, 1, -3, 0),
        (2, 1, 1, 1, 0),
    ]

    assert bellman_ford(edges, 3, 0, 2) is None
