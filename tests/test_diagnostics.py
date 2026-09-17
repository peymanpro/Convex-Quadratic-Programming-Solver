"""Tests for diagnostics module and IPM failure paths."""

from __future__ import annotations

import numpy as np

from solver.diagnostics import Diagnostics, IterationRecord
from solver.ipm import IPMOptions, solve_ipm
from solver.problem import QPProblem


def test_diagnostics_add_and_iterate() -> None:
    d = Diagnostics()
    assert d.iterations == 0
    d.add(IterationRecord(0, 1.0, 1e-3, 1e-3, 1e-3, 1e-1))
    d.add(IterationRecord(1, 0.5, 1e-6, 1e-6, 1e-6, 1e-4))
    assert d.iterations == 2
    recs = d.as_dicts()
    assert recs[0]["iteration"] == 0.0
    assert recs[1]["mu"] == 1e-4


def test_infeasible_returns_max_iter() -> None:
    # Contradictory inequalities: x <= -1 and x >= 1 (via -x <= -1).
    p = QPProblem(
        P=np.eye(1),
        q=np.zeros(1),
        A=np.zeros((0, 1)),
        b=np.zeros(0),
        G=np.array([[1.0], [-1.0]]),
        h=np.array([-1.0, -1.0]),
    )
    opts = IPMOptions(max_iter=10)
    r = solve_ipm(p, opts)
    assert r.status in {"max_iter", "numerical_failure"}


def test_history_has_step_length() -> None:
    p = QPProblem(
        P=np.eye(2),
        q=np.array([-1.0, -1.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([1.0]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    assert any("step_length" in h for h in r.history)


def test_unsolvable_returns_status() -> None:
    p = QPProblem(
        P=np.zeros((2, 2)),
        q=np.array([1.0, 1.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.zeros((1, 2)),
        h=np.array([1.0]),
    )
    r = solve_ipm(p, IPMOptions(max_iter=5))
    assert isinstance(r.status, str)
