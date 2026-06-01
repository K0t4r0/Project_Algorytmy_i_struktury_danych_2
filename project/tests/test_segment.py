from algorithms.segment import (
    SparseTable,
    find_loudest_by_edge,
    find_loudest_by_meters,
    get_distance,
    get_perimeter,
    place_guards,
)
from data_classes.classes import BorderGuard, Mine


def make_square_mines():
    return [
        Mine("A", "gold", 1, (0, 0)),
        Mine("B", "iron", 1, (10, 0)),
        Mine("C", "coal", 1, (10, 10)),
        Mine("D", "copper", 1, (0, 10)),
    ]


def test_get_distance_calculates_euclidean_distance():
    assert get_distance((0, 0), (3, 4)) == 5


def test_get_perimeter_for_square():
    assert get_perimeter(make_square_mines()) == 40


def test_place_guards_sets_positions_and_edges():
    guards = [
        BorderGuard(1, "G1", 10),
        BorderGuard(2, "G2", 20),
        BorderGuard(3, "G3", 30),
        BorderGuard(4, "G4", 40),
    ]

    step, edge_ranges, edge_map = place_guards(make_square_mines(), guards)

    assert step == 10
    assert [guard.position_meters for guard in guards] == [0, 10, 20, 30]
    assert [guard.edge_index for guard in guards] == [0, 1, 2, 3]

    assert edge_ranges == {
        0: [0, 0],
        1: [1, 1],
        2: [2, 2],
        3: [3, 3],
    }

    assert edge_map == {
        ("A", "B"): 0,
        ("B", "C"): 1,
        ("C", "D"): 2,
        ("D", "A"): 3,
    }


def test_sparse_table_query_returns_loudest_guard_in_range():
    guards = [
        BorderGuard(1, "quiet", 10),
        BorderGuard(2, "loud", 99),
        BorderGuard(3, "medium", 50),
    ]
    table = SparseTable(guards)

    result = table.query(0, 2)

    assert result.id == 2
    assert result.loudness == 99


def test_sparse_table_query_returns_none_for_invalid_range():
    table = SparseTable([BorderGuard(1, "G1", 10)])

    assert table.query(1, 0) is None


def test_find_loudest_by_edge_returns_guard_on_selected_edge():
    mines = make_square_mines()
    guards = [
        BorderGuard(1, "G1", 10),
        BorderGuard(2, "G2", 80),
        BorderGuard(3, "G3", 30),
        BorderGuard(4, "G4", 40),
    ]

    _, edge_ranges, edge_map = place_guards(mines, guards)
    table = SparseTable(guards)

    result = find_loudest_by_edge(
        table,
        edge_ranges,
        edge_map,
        mines[1],
        mines[2],
    )

    assert result.id == 2
    assert result.loudness == 80


def test_find_loudest_by_edge_returns_none_for_unknown_edge():
    mines = make_square_mines()
    guards = [
        BorderGuard(1, "G1", 10),
        BorderGuard(2, "G2", 80),
        BorderGuard(3, "G3", 30),
        BorderGuard(4, "G4", 40),
    ]

    _, edge_ranges, edge_map = place_guards(mines, guards)
    table = SparseTable(guards)

    result = find_loudest_by_edge(
        table,
        edge_ranges,
        edge_map,
        mines[0],
        mines[2],
    )

    assert result is None


def test_find_loudest_by_meters_supports_wrapped_range():
    guards = [
        BorderGuard(1, "G1", 10),
        BorderGuard(2, "G2", 20),
        BorderGuard(3, "G3", 30),
        BorderGuard(4, "G4", 90),
    ]

    table = SparseTable(guards)

    result, error = find_loudest_by_meters(guards, table, 10, 25, 5)

    assert error is None
    assert result.id == 4
    assert result.loudness == 90


def test_find_loudest_by_meters_returns_loudest_guard_in_normal_range():
    guards = [
        BorderGuard(1, "G1", 10),
        BorderGuard(2, "G2", 80),
        BorderGuard(3, "G3", 30),
        BorderGuard(4, "G4", 40),
    ]

    table = SparseTable(guards)

    result, error = find_loudest_by_meters(guards, table, 10, 0, 20)

    assert error is None
    assert result.id == 2
    assert result.loudness == 80


def test_find_loudest_by_meters_returns_message_when_no_guards():
    result, error = find_loudest_by_meters([], SparseTable([]), 10, 0, 10)

    assert result is None
    assert error == "No guards available"