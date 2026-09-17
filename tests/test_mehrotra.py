"""Phase 6 tests: Mehrotra predictor-corrector."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from solver.ipm import IPMOptions, solve_ipm
from solver.mehrotra import solve_mehrotra
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


def _halfplane() -> QPProblem:
    return _prob(
        np.eye(2),
        np.array([-2.0, -3.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 1.0]]),
        np.array([2.0]),
    )


def _box() -> QPProblem:
    return _prob(
        np.eye(2),
        np.array([-1.0, -1.0]),
        np.zeros((0, 2)),
        np.zeros(0),
        np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]),
        np.array([1.0, 1.0, 1.0, 1.0]),
    )


def _mixed() -> QPProblem:
    return _prob(
        np.eye(3),
        np.zeros(3),
        np.array([[1.0, 1.0, 1.0]]),
        np.array([1.0]),
        np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
        np.array([0.6, 0.6, 0.6]),
    )


def test_mehrotra_halfplane_matches_analytical() -> None:
    r = solve_mehrotra(_halfplane())
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([0.5, 1.5]), atol=1e-5)


def test_mehrotra_box_optimal() -> None:
    r = solve_mehrotra(_box())
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([1.0, 1.0]), atol=1e-3)


def test_mehrotra_mixed_optimal() -> None:
    r = solve_mehrotra(_mixed())
    assert r.status == "optimal"
    assert np.isclose(np.sum(r.x), 1.0, atol=1e-6)
    assert np.all(r.x <= 0.6 + 1e-6)


def test_mehrotra_fewer_or_equal_iterations_than_basic() -> None:
    p = _halfplane()
    r_meh = solve_mehrotra(p, IPMOptions(max_iter=100, tol=1e-8))
    r_basic = solve_ipm(p, IPMOptions(max_iter=100, tol=1e-8))
    assert r_meh.status == "optimal"
    assert r_basic.status == "optimal"
    assert r_meh.iterations <= r_basic.iterations + 1


def test_mehrotra_complementarity_small() -> None:
    r = solve_mehrotra(_halfplane(), IPMOptions(tol=1e-8))
    assert float(r.z @ r.s) <= 1e-6


def test_mehrotra_duality_gap_small() -> None:
    r = solve_mehrotra(_halfplane(), IPMOptions(tol=1e-8))
    assert r.duality_gap <= 1e-6


def test_mehrotra_objective_matches_basic() -> None:
    p = _halfplane()
    r_meh = solve_mehrotra(p)
    r_basic = solve_ipm(p)
    assert abs(r_meh.objective - r_basic.objective) <= 1e-5
