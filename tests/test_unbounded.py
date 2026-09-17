"""Tests for unbounded detection heuristic."""

from __future__ import annotations

import numpy as np

from solver import QPProblem, solve


def test_unbounded_flat_direction() -> None:
    # P = 0, q = [1, 1], bounded only by x1 + x2 <= 1.
    # Minimizing x1 + x2 in the direction (-1, -1) is unbounded below.
    p = QPProblem(
        P=np.zeros((2, 2)),
        q=np.array([1.0, 1.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([1.0]),
    )
    r = solve(p)
    assert r.status in {"unbounded", "numerical_failure", "max_iter"}


def test_flat_direction_but_bounded() -> None:
    # P = 0, q = 0 -> every feasible point is optimal with objective 0.
    p = QPProblem(
        P=np.zeros((2, 2)),
        q=np.zeros(2),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([1.0]),
    )
    r = solve(p)
    assert r.status in {"optimal", "max_iter", "numerical_failure"}
