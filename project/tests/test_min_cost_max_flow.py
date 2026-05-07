import pytest

from data_classes.classes import Dwarf, Mine
from algorithms.min_cost_max_flow import MCMF
from tools.data_manager import data_store


def test_mcmf_creation():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(3, 4))
    ]

    solver = MCMF(dwarves, mines)

    assert solver.dwarves == dwarves
    assert solver.mines == mines
    assert solver.S == 0
    assert solver.T == 3
    assert solver.nodes_count == 4
    assert solver.graph == []


def test_get_distance():
    solver = MCMF([], [])

    distance = solver.get_distance((0, 0), (3, 4))

    assert distance == 5


def test_add_edge_creates_forward_and_reverse_edges():
    solver = MCMF([], [])

    solver.add_edge(0, 1, 5, 10)

    assert len(solver.graph) == 2

    forward_edge = solver.graph[0]
    reverse_edge = solver.graph[1]

    assert forward_edge[0] == 0
    assert forward_edge[1] == 1
    assert forward_edge[2] == 5
    assert forward_edge[3] == 10
    assert forward_edge[4] == 1

    assert reverse_edge[0] == 1
    assert reverse_edge[1] == 0
    assert reverse_edge[2] == 0
    assert reverse_edge[3] == -10
    assert reverse_edge[4] == 0


def test_build_network_adds_source_to_dwarf_edge():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    assert [0, 1, 1, 0, 1] in solver.graph


def test_build_network_adds_dwarf_to_mine_edge_when_skill_matches():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(3, 4))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    dwarf_node = 1
    mine_node = 2

    matching_edges = [
        edge for edge in solver.graph
        if edge[0] == dwarf_node and edge[1] == mine_node
    ]

    assert len(matching_edges) == 1
    assert matching_edges[0][2] == 1
    assert matching_edges[0][3] == 5


def test_build_network_does_not_add_dwarf_to_mine_edge_when_skill_does_not_match():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="iron", capacity=1, pos=(3, 4))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    dwarf_node = 1
    mine_node = 2

    matching_edges = [
        edge for edge in solver.graph
        if edge[0] == dwarf_node and edge[1] == mine_node
    ]

    assert len(matching_edges) == 0


def test_build_network_adds_mine_to_sink_edge_with_capacity():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=3, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    mine_node = 2
    sink_node = solver.T

    matching_edges = [
        edge for edge in solver.graph
        if edge[0] == mine_node and edge[1] == sink_node
    ]

    assert len(matching_edges) == 1
    assert matching_edges[0][2] == 3
    assert matching_edges[0][3] == 0


def test_build_network_sets_source_and_sink_positions_in_data_store():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(10, 10))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(30, 20))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    assert data_store.s_pos == (0, 15)
    assert data_store.t_pos == (40, 15)


def test_solve_generator_finds_one_assignment():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert len(steps) == 1

    final_paths = steps[-1]

    assert (data_store.s_pos, (0, 0)) in final_paths
    assert ((0, 0), (10, 0)) in final_paths
    assert ((10, 0), data_store.t_pos) in final_paths


def test_solve_generator_does_not_assign_dwarf_without_matching_skill():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="iron", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert steps == []


def test_solve_generator_respects_mine_capacity():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0)),
        Dwarf(id=2, name="Balin", skills=["gold"], value=90, home_pos=(0, 10)),
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert len(steps) == 1


def test_solve_generator_can_assign_two_dwarves_when_capacity_allows():
    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], value=100, home_pos=(0, 0)),
        Dwarf(id=2, name="Balin", skills=["gold"], value=90, home_pos=(0, 10)),
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=2, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert len(steps) == 2