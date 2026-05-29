import pytest

from algorithms.royal_border_patrol import RoyalBorderPatrol


def normalize(points):
    return set(points)


def test_get_border_route_with_graham_returns_outer_points():
    patrol = RoyalBorderPatrol([
        (0, 0),
        (2, 0),
        (2, 2),
        (0, 2),
        (1, 1),
    ])

    route = patrol.get_border_route("graham")

    assert normalize(route) == {(0, 0), (2, 0), (2, 2), (0, 2)}
    assert (1, 1) not in route


def test_get_border_route_with_jarvis_returns_outer_points():
    patrol = RoyalBorderPatrol()
    patrol.load_data([
        (0, 0),
        (2, 0),
        (2, 2),
        (0, 2),
        (1, 1),
    ])

    route = patrol.get_border_route("jarvis")

    assert normalize(route) == {(0, 0), (2, 0), (2, 2), (0, 2)}
    assert (1, 1) not in route


def test_add_mine_adds_point_to_patrol_data():
    patrol = RoyalBorderPatrol()

    patrol.add_mine(3, 4)

    assert patrol.points == [(3, 4)]


def test_unknown_algorithm_raises_value_error():
    patrol = RoyalBorderPatrol([(0, 0), (1, 1), (2, 0)])

    with pytest.raises(ValueError):
        patrol.get_border_route("unknown")
