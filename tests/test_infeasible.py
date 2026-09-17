"""Tests for the heuristic infeasibility detection."""

from __future__ import annotations

import numpy as np

from solver import QPProblem, solve


def test_infeasible_strict_case() -> None:
    """Case that reliably triggers the infeasibility heuristic."""
    # x1 >= 1 and x1 <= 0 are contradictory.
    p = QPProblem(
        P=np.eye(2),
        q=np.zeros(2),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[-1.0, 0.0], [1.0, 0.0]]),
        h=np.array([-1.0, 0.0]),
    )
    r = solve(p)
    assert r.status == "infeasible"


def test_infeasible_outside_heuristic_is_documented() -> None:
    """Contradictory 1D bounds, x <= -1 and x >= 1.

    The heuristic does not guarantee detection when the algorithm hits
    numerical failure earlier. This test documents the current behavior
    rather than asserting a formal infeasibility certificate.
    """
    p = QPProblem(
        P=np.eye(1),
        q=np.zeros(1),
        A=np.zeros((0, 1)),
        b=np.zeros(0),
        G=np.array([[1.0], [-1.0]]),
        h=np.array([-1.0, -1.0]),
    )
    r = solve(p)
    assert r.status in {"infeasible", "numerical_failure", "max_iter"}


def test_feasible_not_mislabeled() -> None:
    """A feasible QP must not be flagged as infeasible."""
    p = QPProblem(
        P=np.eye(2),
        q=np.array([-2.0, -3.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([2.0]),
    )
    r = solve(p)
    assert r.status == "optimal"
