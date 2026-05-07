import pytest

from algorithms.hull import (
    get_orientation,
    dist_sq,
    graham_scan,
    jarvis,
    jarvis_generator,
    graham_generator,
)


def test_get_orientation_straight():
    assert get_orientation((0, 0), (1, 0), (2, 0)) == 0


def test_get_orientation_right_turn():
    assert get_orientation((0, 0), (1, 0), (1, -1)) == 1


def test_get_orientation_left_turn():
    assert get_orientation((0, 0), (1, 0), (1, 1)) == 2


def test_dist_sq():
    assert dist_sq((0, 0), (3, 4)) == 25
    assert dist_sq((2, 2), (2, 2)) == 0


def test_graham_scan_returns_same_points_when_less_than_three():
    points = [(0, 0), (1, 1)]
    assert graham_scan(points) == points


def test_graham_scan_square_with_inner_point():
    points = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]

    hull = graham_scan(points)

    assert set(hull) == {(0, 0), (0, 2), (2, 0), (2, 2)}
    assert (1, 1) not in hull
    assert len(hull) == 4


def test_graham_scan_ignores_points_on_same_edge():
    points = [(0, 0), (1, 0), (2, 0), (0, 2), (2, 2), (1, 1)]

    hull = graham_scan(points)

    assert set(hull) == {(0, 0), (2, 0), (2, 2), (0, 2)}
    assert (1, 0) not in hull
    assert len(hull) == 4


def test_jarvis_generator_returns_closed_hull():
    points = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]

    steps = list(jarvis_generator(points))
    final_hull, current_point = steps[-1]

    assert current_point is None
    assert final_hull[0] == final_hull[-1]
    assert set(final_hull[:-1]) == {(0, 0), (0, 2), (2, 0), (2, 2)}
    assert (1, 1) not in final_hull


def test_graham_generator_returns_closed_hull():
    points = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]

    steps = list(graham_generator(points))
    final_hull, current_point = steps[-1]

    assert current_point is None
    assert final_hull[0] == final_hull[-1]
    assert set(final_hull[:-1]) == {(0, 0), (0, 2), (2, 0), (2, 2)}
    assert (1, 1) not in final_hull


def test_generators_return_points_when_less_than_three():
    points = [(0, 0), (1, 1)]

    assert list(jarvis_generator(points)) == [(points, None)]
    assert list(graham_generator(points)) == [(points, None)]


def test_jarvis_function_returns_closed_hull_for_valid_input():
    points = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]

    steps = list(jarvis(points))
    final_hull, current_point = steps[-1]

    assert current_point is None
    assert final_hull[0] == final_hull[-1]
    assert set(final_hull[:-1]) == {(0, 0), (0, 2), (2, 0), (2, 2)}
    assert (1, 1) not in final_hull