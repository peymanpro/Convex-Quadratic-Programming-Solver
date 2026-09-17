"""Phase 7 tests: sparse KKT equivalence and numerical safeguards."""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from solver.ipm import IPMOptions, solve_ipm
from solver.linear_solver import (
    LinearSolverOptions,
    assemble_kkt,
    factor_and_solve,
)
from solver.mehrotra import solve_mehrotra
from solver.problem import QPProblem


def _halfplane() -> QPProblem:
    return QPProblem(
        P=np.eye(2),
        q=np.array([-2.0, -3.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([2.0]),
    )


def test_sparse_kkt_matches_dense() -> None:
    P = np.eye(2)
    A = np.array([[1.0, 1.0]])
    G = np.array([[1.0, -1.0]])
    W = np.array([0.5])
    K_dense = assemble_kkt(P, A, G, W, 0.0, backend="dense")
    K_sparse = assemble_kkt(P, A, G, W, 0.0, backend="sparse")
    assert sp.issparse(K_sparse)
    assert np.allclose(K_sparse.toarray(), K_dense)


def test_sparse_kkt_no_equalities() -> None:
    P = np.eye(2)
    A = np.zeros((0, 2))
    G = np.array([[1.0, 0.0]])
    W = np.array([1.0])
    K_sp = assemble_kkt(P, A, G, W, 0.0, backend="sparse")
    H = P + G.T @ (W[:, None] * G)
    assert np.allclose(np.asarray(K_sp.todense()), H)


def test_factor_and_solve_dense_matches_numpy() -> None:
    rng = np.random.default_rng(0)
    M = rng.standard_normal((5, 5))
    K = M @ M.T + 5.0 * np.eye(5)
    rhs = rng.standard_normal(5)
    sol = factor_and_solve(K, rhs, LinearSolverOptions(backend="dense"))
    ref = np.linalg.solve(K, rhs)
    assert np.allclose(sol, ref)


def test_factor_and_solve_sparse_matches_dense() -> None:
    rng = np.random.default_rng(1)
    M = rng.standard_normal((8, 8))
    K = M @ M.T + 5.0 * np.eye(8)
    rhs = rng.standard_normal(8)
    sol_d = factor_and_solve(K, rhs, LinearSolverOptions(backend="dense"))
    sol_s = factor_and_solve(K, rhs, LinearSolverOptions(backend="sparse"))
    assert np.allclose(sol_d, sol_s, atol=1e-10)


def test_sparse_auto_backend_threshold() -> None:
    rng = np.random.default_rng(2)
    M = rng.standard_normal((20, 20))
    K = M @ M.T + 10.0 * np.eye(20)
    rhs = rng.standard_normal(20)
    sol = factor_and_solve(
        K, rhs, LinearSolverOptions(backend="dense", sparse_threshold=10)
    )
    ref = np.linalg.solve(K, rhs)
    assert np.allclose(sol, ref, atol=1e-10)


def test_ill_conditioned_still_solves() -> None:
    P = np.diag([1e-6, 1e-4, 1e-2])
    q = np.array([-1.0, -2.0, -3.0])
    A = np.zeros((0, 3))
    b = np.zeros(0)
    G = np.array([[1.0, 1.0, 1.0]])
    h = np.array([10.0])
    p = QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)
    r = solve_ipm(p, IPMOptions(max_iter=200, tol=1e-7))
    assert r.status == "optimal"


def test_ill_conditioned_mehrotra() -> None:
    P = np.diag([1e-6, 1e-4, 1e-2])
    q = np.array([-1.0, -2.0, -3.0])
    A = np.zeros((0, 3))
    b = np.zeros(0)
    G = np.array([[1.0, 1.0, 1.0]])
    h = np.array([10.0])
    p = QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)
    r = solve_mehrotra(p, IPMOptions(max_iter=200, tol=1e-7))
    assert r.status == "optimal"


def test_condition_number_reasonable() -> None:
    P = np.eye(4)
    G = np.array([[1.0, 0.0, 0.0, 0.0]])
    W = np.array([1.0])
    K = np.asarray(
        assemble_kkt(P, np.zeros((0, 4)), G, W, 0.0, backend="sparse").todense()
    )
    assert np.linalg.cond(K) < 1e6


def test_singular_sparse_raises() -> None:
    K = np.zeros((3, 3))
    rhs = np.ones(3)
    try:
        factor_and_solve(K, rhs, LinearSolverOptions(backend="sparse"))
    except Exception as exc:
        assert "Sparse LU failed" in str(exc) or "singular" in str(exc).lower()
    else:
        # Some platforms return without error; require at least the fallback
        raise AssertionError("expected failure on singular matrix")
