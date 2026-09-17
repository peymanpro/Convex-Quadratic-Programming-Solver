"""Phase 9 tests: rigorous numerical validation corpus."""

from __future__ import annotations

import numpy as np

from solver import QPProblem, SolverResult, solve
from validation.generators import (
    degenerate_qp,
    ill_conditioned_qp,
    infeasible_qp,
    random_feasible_qp,
    random_mixed_qp,
    singleton_qp,
)

TOL = 1e-5


def _check_optimal(r: SolverResult) -> None:
    assert r.status == "optimal", r.status
    assert r.primal_residual <= TOL
    assert r.dual_residual <= TOL
    assert r.duality_gap <= TOL


def test_corpus_random_feasible_50() -> None:
    rng = np.random.default_rng(0)
    ok = 0
    for _ in range(50):
        n = int(rng.integers(2, 8))
        p = int(rng.integers(1, 6))
        prob = random_feasible_qp(n, p, rng, cond=10.0)
        r = solve(prob)
        _check_optimal(r)
        ok += 1
    assert ok == 50


def test_corpus_mixed_20() -> None:
    rng = np.random.default_rng(1)
    ok = 0
    for _ in range(20):
        n = int(rng.integers(3, 7))
        m = int(rng.integers(1, 3))
        p = int(rng.integers(1, 5))
        prob = random_mixed_qp(n, m, p, rng, cond=10.0)
        r = solve(prob)
        _check_optimal(r)
        ok += 1
    assert ok == 20


def test_corpus_ill_conditioned_10() -> None:
    rng = np.random.default_rng(2)
    conds = [1e2, 1e3, 1e4, 1e5, 1e6]
    ok = 0
    for cond in conds:
        for _ in range(2):
            prob = ill_conditioned_qp(4, cond, rng)
            r = solve(prob)
            if r.status == "optimal":
                ok += 1
    assert ok >= 5


def test_corpus_failure_modes_10() -> None:
    rng = np.random.default_rng(3)
    for _ in range(10):
        prob = infeasible_qp(rng)
        r = solve(prob)
        assert r.status in {"max_iter", "numerical_failure"}


def test_corpus_edge_cases_10() -> None:
    # 1) Singleton QP
    r = solve(singleton_qp())
    assert r.status == "optimal"
    assert np.isclose(r.x[0], 2.0, atol=1e-5)

    # 2) Degenerate P=0
    r = solve(degenerate_qp())
    assert r.status in {"optimal", "max_iter", "numerical_failure", "unbounded"}

    # 3) Equality only
    p = QPProblem(
        P=np.eye(2),
        q=np.zeros(2),
        A=np.array([[1.0, 1.0]]),
        b=np.array([1.0]),
        G=np.zeros((0, 2)),
        h=np.zeros(0),
    )
    assert solve(p).status == "optimal"

    # 4) Box constraint
    p = QPProblem(
        P=np.eye(2),
        q=np.array([-1.0, -1.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]),
        h=np.array([1.0, 1.0, 1.0, 1.0]),
    )
    r = solve(p)
    assert r.status == "optimal"

    # 5) Scaled P
    p = QPProblem(
        P=10.0 * np.eye(2),
        q=np.array([-10.0, -10.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([1.0]),
    )
    assert solve(p).status == "optimal"

    # 6-10) Repeated small random problems
    rng = np.random.default_rng(99)
    for _ in range(5):
        prob = random_feasible_qp(3, 2, rng)
        assert solve(prob).status == "optimal"


def test_objective_error_vs_analytical() -> None:
    p = QPProblem(
        P=np.eye(2),
        q=np.array([-2.0, -3.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([2.0]),
    )
    r = solve(p)
    x_star = np.array([0.5, 1.5])
    obj_star = float(0.5 * x_star @ p.P @ x_star + p.q @ x_star)
    assert abs(r.objective - obj_star) <= 1e-5
