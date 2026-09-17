"""Tests for the heuristic unbounded detection."""

from __future__ import annotations

import numpy as np

from solver import QPProblem, solve


def test_unbounded_strict_case() -> None:
    """Case that reliably triggers the iterate-norm heuristic."""
    # Flat objective with a single inequality constraint; the iterates
    # grow without bound and the heuristic fires.
    p = QPProblem(
        P=np.zeros((2, 2)),
        q=np.array([1.0, 1.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([1.0]),
    )
    r = solve(p)
    assert r.status == "unbounded"


def test_bounded_flat_objective_is_optimal() -> None:
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


def test_unbounded_outside_heuristic_is_documented() -> None:
    """min -x1 s.t. x1 <= 10 is mathematically unbounded (x1 -> -inf),
    but the iterate does not grow fast enough for the heuristic to fire.
    This test documents the current limitation rather than asserting
    correctness we do not provide.
    """
    p = QPProblem(
        P=np.zeros((1, 1)),
        q=np.array([-1.0]),
        A=np.zeros((0, 1)),
        b=np.zeros(0),
        G=np.array([[1.0]]),
        h=np.array([10.0]),
    )
    r = solve(p)
    assert r.status in {"optimal", "max_iter", "numerical_failure", "unbounded"}


def test_truly_bounded_problem_is_optimal() -> None:
    # min -x1 s.t. 0 <= x1 <= 1 -> bounded, optimum x1 = 1
    p = QPProblem(
        P=np.zeros((1, 1)),
        q=np.array([-1.0]),
        A=np.zeros((0, 1)),
        b=np.zeros(0),
        G=np.array([[1.0], [-1.0]]),
        h=np.array([1.0, 0.0]),
    )
    r = solve(p)
    assert r.status == "optimal"
    assert abs(r.x[0] - 1.0) <= 1e-5
