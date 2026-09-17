"""Phase 10 tests: Hypothesis-based property tests."""

from __future__ import annotations

import numpy as np
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from solver import QPProblem, solve

TOL = 1e-5


def _make_psd(n: int, rng: np.random.Generator, cond: float = 10.0) -> np.ndarray:
    Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    eigs = np.logspace(0.0, np.log10(cond), n)
    return (Q * eigs) @ Q.T


@settings(
    max_examples=40,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
@given(
    n=st.integers(min_value=2, max_value=6),
    p=st.integers(min_value=1, max_value=4),
    seed=st.integers(min_value=0, max_value=10_000),
)
def test_kkt_holds_for_random_feasible_qp(n: int, p: int, seed: int) -> None:
    rng = np.random.default_rng(seed)
    P = _make_psd(n, rng)
    q = rng.standard_normal(n)
    x0 = rng.standard_normal(n)
    G = rng.standard_normal((p, n))
    h = G @ x0 + rng.uniform(0.5, 2.0, size=p)
    problem = QPProblem(
        P=P,
        q=q,
        A=np.zeros((0, n)),
        b=np.zeros(0),
        G=G,
        h=h,
    )
    r = solve(problem)
    assert r.status == "optimal"
    # KKT: stationarity + primal feasibility + complementarity
    assert r.primal_residual <= TOL
    assert r.dual_residual <= TOL
    assert r.duality_gap <= TOL


@settings(
    max_examples=40,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
@given(seed=st.integers(min_value=0, max_value=10_000))
def test_feasibility_preserved(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n, p = 4, 3
    P = _make_psd(n, rng)
    q = rng.standard_normal(n)
    x0 = rng.standard_normal(n)
    G = rng.standard_normal((p, n))
    h = G @ x0 + rng.uniform(1.0, 2.0, size=p)
    problem = QPProblem(
        P=P,
        q=q,
        A=np.zeros((0, n)),
        b=np.zeros(0),
        G=G,
        h=h,
    )
    r = solve(problem)
    if r.status != "optimal":
        return
    slack = h - G @ r.x
    assert np.all(slack >= -TOL)


@settings(max_examples=30, deadline=None)
@given(scale=st.floats(min_value=0.01, max_value=100.0))
def test_scaling_invariance(scale: float) -> None:
    # Scaling both P and q by s should not change the optimal x.
    P = np.eye(2)
    q = np.array([-2.0, -3.0])
    G = np.array([[1.0, 1.0]])
    h = np.array([2.0])
    p1 = QPProblem(P=P, q=q, A=np.zeros((0, 2)), b=np.zeros(0), G=G, h=h)
    p2 = QPProblem(
        P=scale * P,
        q=scale * q,
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=G,
        h=h,
    )
    r1 = solve(p1)
    r2 = solve(p2)
    if r1.status == "optimal" and r2.status == "optimal":
        assert np.allclose(r1.x, r2.x, atol=1e-3)


@settings(max_examples=30, deadline=None)
@given(seed=st.integers(min_value=0, max_value=10_000))
def test_objective_matches_manual_evaluation(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n, p = 3, 2
    P = _make_psd(n, rng)
    q = rng.standard_normal(n)
    x0 = rng.standard_normal(n)
    G = rng.standard_normal((p, n))
    h = G @ x0 + rng.uniform(0.5, 2.0, size=p)
    problem = QPProblem(
        P=P,
        q=q,
        A=np.zeros((0, n)),
        b=np.zeros(0),
        G=G,
        h=h,
    )
    r = solve(problem)
    if r.status != "optimal":
        return
    manual = float(0.5 * r.x @ P @ r.x + q @ r.x)
    assert abs(r.objective - manual) <= TOL
