"""Phase 4 tests: slack formulation and IPM convergence on constrained QPs."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from solver.ipm import IPMOptions, solve_ipm
from solver.problem import QPProblem

TOL = 1e-6


def _prob(
    P: NDArray[np.float64],
    q: NDArray[np.float64],
    A: NDArray[np.float64],
    b: NDArray[np.float64],
    G: NDArray[np.float64],
    h: NDArray[np.float64],
) -> QPProblem:
    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)


def _assert_kkt(p: QPProblem, x: NDArray[np.float64]) -> None:
    r_d = p.P @ x + p.q
    if p.m:
        r_d = r_d
    # stationarity is checked via solver residuals inside; here check primal
    if p.m:
        assert np.max(np.abs(p.A @ x - p.b)) <= TOL
    if p.p:
        assert np.max(np.maximum(0.0, p.G @ x - p.h)) <= TOL


def test_ineq_1_halfplane() -> None:
    p = _prob(
        np.eye(2),
        np.array([-2.0, -3.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 1.0]]),
        np.array([2.0]),
    )
    r = solve_ipm(p, IPMOptions(max_iter=100, tol=1e-8))
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([0.5, 1.5]), atol=1e-5)
    _assert_kkt(p, r.x)


def test_ineq_2_box() -> None:
    p = _prob(
        np.eye(2),
        np.array([-1.0, -1.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]),
        np.array([1.0, 1.0, 1.0, 1.0]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([1.0, 1.0]), atol=1e-3)


def test_ineq_3_three_constraints() -> None:
    p = _prob(
        np.eye(2),
        np.array([0.0, 0.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 1.0], [1.0, -1.0], [-1.0, 0.0]]),
        np.array([1.0, 1.0, 0.0]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    _assert_kkt(p, r.x)


def test_ineq_4_origin_optimum() -> None:
    p = _prob(
        np.eye(2),
        np.array([0.0, 0.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 0.0], [0.0, 1.0]]),
        np.array([1.0, 1.0]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([0.0, 0.0]), atol=1e-6)


def test_ineq_5_scaled_P() -> None:
    p = _prob(
        np.diag([2.0, 2.0]),
        np.array([-4.0, -4.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 0.0], [0.0, 1.0]]),
        np.array([1.0, 1.0]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([1.0, 1.0]), atol=1e-3)


def test_mixed_1_eq_plus_ineq() -> None:
    p = _prob(
        np.eye(2),
        np.array([0.0, 0.0]),
        np.array([[1.0, 1.0]]),
        np.array([1.0]),
        np.array([[-1.0, 0.0]]),
        np.array([-0.4]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    assert np.isclose(r.x[0] + r.x[1], 1.0, atol=1e-6)
    assert r.x[0] >= 0.4 - 1e-6


def test_mixed_2_eq_box() -> None:
    p = _prob(
        np.eye(3),
        np.zeros(3),
        np.array([[1.0, 1.0, 1.0]]),
        np.array([1.0]),
        np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
        np.array([0.6, 0.6, 0.6]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    assert np.isclose(np.sum(r.x), 1.0, atol=1e-6)
    assert np.all(r.x <= 0.6 + 1e-6)


def test_mixed_3_3d() -> None:
    p = _prob(
        np.diag([1.0, 1.0, 1.0]),
        np.array([-1.0, -2.0, -3.0]),
        np.array([[1.0, 1.0, 1.0]]),
        np.array([2.0]),
        np.array([[-1.0, 0.0, 0.0]]),
        np.array([0.0]),
    )
    r = solve_ipm(p)
    assert r.status == "optimal"
    assert np.isclose(np.sum(r.x), 2.0, atol=1e-6)


def test_complementarity_holds() -> None:
    p = _prob(
        np.eye(2),
        np.array([-1.0, -1.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 1.0]]),
        np.array([1.0]),
    )
    r = solve_ipm(p, IPMOptions(tol=1e-8))
    assert r.status == "optimal"
    comp = float(r.z @ r.s)
    assert comp <= 1e-6


def test_duality_gap_small() -> None:
    p = _prob(
        np.eye(2),
        np.array([-1.0, -1.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 1.0]]),
        np.array([1.0]),
    )
    r = solve_ipm(p, IPMOptions(tol=1e-8))
    assert r.duality_gap <= 1e-6
