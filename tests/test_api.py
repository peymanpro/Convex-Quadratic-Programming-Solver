"""Phase 8 tests: public API."""

from __future__ import annotations

import numpy as np
import pytest

from solver import (
    DimensionMismatch,
    IPMOptions,
    NonConvexProblem,
    QPProblem,
    SolverResult,
    __version__,
    solve,
)


def _halfplane() -> QPProblem:
    return QPProblem(
        P=np.eye(2),
        q=np.array([-2.0, -3.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([2.0]),
    )


def test_version_exposed() -> None:
    assert __version__ == "0.2.0"


def test_solve_returns_solver_result() -> None:
    r = solve(_halfplane())
    assert isinstance(r, SolverResult)
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([0.5, 1.5]), atol=1e-5)


def test_solve_result_fields_populated() -> None:
    r = solve(_halfplane())
    assert r.solve_time >= 0.0
    assert r.iterations >= 0
    assert r.duality_gap <= 1e-6
    assert r.primal_residual <= 1e-6
    assert r.dual_residual <= 1e-6
    assert r.y.shape == (0,)
    assert r.z.shape == (1,)
    assert r.s.shape == (1,)


def test_solve_method_ipm() -> None:
    r = solve(_halfplane(), method="ipm")
    assert r.status == "optimal"


def test_solve_method_invalid_raises() -> None:
    with pytest.raises(ValueError):
        solve(_halfplane(), method="nope")


def test_solve_nonconvex_raises() -> None:
    p = QPProblem(
        P=np.array([[1.0, 0.0], [0.0, -1.0]]),
        q=np.zeros(2),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.zeros((0, 2)),
        h=np.zeros(0),
    )
    with pytest.raises(NonConvexProblem):
        solve(p)


def test_solve_dimension_mismatch_raises() -> None:
    p = QPProblem(
        P=np.eye(2),
        q=np.zeros(3),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.zeros((0, 2)),
        h=np.zeros(0),
    )
    with pytest.raises(DimensionMismatch):
        solve(p)


def test_solve_options_forwarded() -> None:
    r = solve(_halfplane(), options=IPMOptions(tol=1e-9))
    assert r.status == "optimal"
    assert r.duality_gap <= 1e-8
