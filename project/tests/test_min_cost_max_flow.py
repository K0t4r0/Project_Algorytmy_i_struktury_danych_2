import pytest

from data_classes.classes import Dwarf, Mine
from algorithms.min_cost_max_flow import MCMF


class FakeDataStore:
    def __init__(self):
        self.s_pos = None
        self.t_pos = None
        self.flow_paths = []


def test_mcmf_creation():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(3, 4))
    ]

    solver = MCMF(dwarves, mines, data_store)

    assert solver.dwarves == dwarves
    assert solver.mines == mines
    assert solver.S == 0
    assert solver.T == 3
    assert solver.nodes_count == 4
    assert solver.graph == []
    assert solver.data_store == data_store


def test_get_distance():
    data_store = FakeDataStore()
    solver = MCMF([], [], data_store)

    distance = solver.get_distance((0, 0), (3, 4))

    assert distance == 25


def test_add_edge_creates_forward_and_reverse_edges():
    data_store = FakeDataStore()
    solver = MCMF([], [], data_store)

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
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    assert [0, 1, 1, 0, 1] in solver.graph


def test_build_network_adds_dwarf_to_mine_edge_when_skill_matches():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(3, 4))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    dwarf_node = 1
    mine_node = 2

    matching_edges = [
        edge for edge in solver.graph
        if edge[0] == dwarf_node and edge[1] == mine_node
    ]

    assert len(matching_edges) == 1
    assert matching_edges[0][2] == 1
    assert matching_edges[0][3] == 25


def test_build_network_does_not_add_dwarf_to_mine_edge_when_skill_does_not_match():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="iron", capacity=1, pos=(3, 4))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    dwarf_node = 1
    mine_node = 2

    matching_edges = [
        edge for edge in solver.graph
        if edge[0] == dwarf_node and edge[1] == mine_node
    ]

    assert len(matching_edges) == 0


def test_build_network_adds_mine_to_sink_edge_with_capacity():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=3, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
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
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(10, 10))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(30, 20))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    assert data_store.s_pos == (0, 15)
    assert data_store.t_pos == (40, 15)


def test_get_current_paths_returns_empty_list_before_solving():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    paths = solver.get_current_paths()

    assert paths == []


def test_solve_generator_finds_one_assignment():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert len(steps) == 1

    first_step = steps[0]

    assert first_step["step"] == 1
    assert first_step["step_cost"] == 100
    assert first_step["total_cost_so_far"] == 100
    assert "Gimli" in first_step["action"]
    assert "gold" in first_step["action"]
    assert first_step["paths"] == data_store.flow_paths

    assert (data_store.s_pos, (0, 0)) in first_step["paths"]
    assert ((0, 0), (10, 0)) in first_step["paths"]
    assert ((10, 0), data_store.t_pos) in first_step["paths"]


def test_solve_generator_does_not_assign_dwarf_without_matching_skill():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="iron", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert steps == []
    assert data_store.flow_paths == []


def test_solve_generator_respects_mine_capacity():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0)),
        Dwarf(id=2, name="Balin", skills=["gold"], home_pos=(0, 10)),
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert len(steps) == 1

    final_paths = steps[-1]["paths"]

    dwarf_to_mine_paths = [
        path for path in final_paths
        if path[0] in [(0, 0), (0, 10)] and path[1] == (10, 0)
    ]

    assert len(dwarf_to_mine_paths) == 1


def test_solve_generator_can_assign_two_dwarves_when_capacity_allows():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0)),
        Dwarf(id=2, name="Balin", skills=["gold"], home_pos=(0, 10)),
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=2, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert len(steps) == 2

    final_step = steps[-1]

    assert final_step["step"] == 2
    assert final_step["total_cost_so_far"] == 300.0

    final_paths = final_step["paths"]

    dwarf_to_mine_paths = [
        path for path in final_paths
        if path[0] in [(0, 0), (0, 10)] and path[1] == (10, 0)
    ]

    assert len(dwarf_to_mine_paths) == 2


def test_solve_generator_without_gui_does_not_update_data_store_flow_paths():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    steps = list(solver.solve_generator(is_use_gui=False))

    assert len(steps) == 1
    assert steps[0]["paths"] != []
    assert data_store.flow_paths == []


def test_solve_generator_step_data_has_expected_keys():
    data_store = FakeDataStore()

    dwarves = [
        Dwarf(id=1, name="Gimli", skills=["gold"], home_pos=(0, 0))
    ]
    mines = [
        Mine(id="M-01", mine_type="gold", capacity=1, pos=(10, 0))
    ]

    solver = MCMF(dwarves, mines, data_store)
    solver.build_network()

    steps = list(solver.solve_generator())

    assert len(steps) == 1

    step = steps[0]

    assert set(step.keys()) == {
        "step",
        "action",
        "step_cost",
        "total_cost_so_far",
        "paths",
    }