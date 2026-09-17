"""Tests for the equality-constrained KKT solver."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from solver.kkt import solve_equality_qp
from solver.problem import QPProblem
from solver.residuals import compute_residuals

TOL = 1e-9


def _wrap(
    P: NDArray[np.float64],
    q: NDArray[np.float64],
    A: NDArray[np.float64],
    b: NDArray[np.float64],
) -> QPProblem:
    n = P.shape[0]
    return QPProblem(
        P=P,
        q=q,
        A=A,
        b=b,
        G=np.zeros((0, n)),
        h=np.zeros(0),
    )


def _check(
    p: QPProblem,
    expected_x: NDArray[np.float64],
    expected_nu: NDArray[np.float64],
) -> None:
    sol = solve_equality_qp(p)
    assert np.allclose(sol.x, expected_x, atol=TOL)
    if expected_nu.size:
        assert np.allclose(sol.nu, expected_nu, atol=TOL)
    lam = np.zeros(p.G.shape[0])
    res = compute_residuals(p.P, p.q, p.A, p.b, p.G, p.h, sol.x, sol.nu, lam)
    assert res.stationarity <= TOL
    assert res.primal_eq <= TOL


def test_eq_1_unconstrained() -> None:
    p = _wrap(
        np.eye(2),
        np.array([-1.0, -2.0]),
        np.zeros((0, 2)),
        np.zeros(0),
    )
    _check(p, np.array([1.0, 2.0]), np.zeros(0))


def test_eq_2_sum_constraint() -> None:
    p = _wrap(
        np.eye(2),
        np.zeros(2),
        np.array([[1.0, 1.0]]),
        np.array([1.0]),
    )
    _check(p, np.array([0.5, 0.5]), np.array([-0.5]))


def test_eq_3_two_equalities_3d() -> None:
    P = np.eye(3)
    q = np.zeros(3)
    A = np.array([[1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    b = np.array([1.0, 2.0])
    sol = solve_equality_qp(_wrap(P, q, A, b))
    assert np.isclose(sol.x[2], 2.0, atol=TOL)
    assert np.isclose(sol.x[0] + sol.x[1], 1.0, atol=TOL)
    assert np.isclose(sol.x[0], sol.x[1], atol=TOL)


def test_eq_4_diagonal_P() -> None:
    P = np.diag([2.0, 4.0])
    q = np.array([-2.0, -8.0])
    A = np.array([[1.0, 1.0]])
    b = np.array([3.0])
    sol = solve_equality_qp(_wrap(P, q, A, b))
    lam = np.zeros(0)
    res = compute_residuals(
        P, q, A, b, np.zeros((0, 2)), np.zeros(0), sol.x, sol.nu, lam
    )
    assert res.stationarity <= TOL
    assert res.primal_eq <= TOL


def test_eq_5_3d_identity() -> None:
    P = np.eye(3)
    q = np.zeros(3)
    A = np.array([[1.0, 1.0, 1.0]])
    b = np.array([3.0])
    _check(
        p=_wrap(P, q, A, b),
        expected_x=np.array([1.0, 1.0, 1.0]),
        expected_nu=np.array([-1.0]),
    )
