"""Equality-constrained KKT system and sparse KKT builders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from solver.exceptions import NumericalFailure
from solver.problem import QPProblem


@dataclass(frozen=True)
class EqualityKKTSolution:
    """Solution of the equality-constrained KKT system."""

    x: NDArray[np.float64]
    nu: NDArray[np.float64]


def build_equality_kkt(
    P: NDArray[np.float64],
    A: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Assemble K = [[P, A^T], [A, 0]]."""
    n = P.shape[0]
    m = A.shape[0]
    K = np.zeros((n + m, n + m), dtype=np.float64)
    K[:n, :n] = P
    if m:
        K[:n, n:] = A.T
        K[n:, :n] = A
    return K


def solve_equality_qp(problem: QPProblem) -> EqualityKKTSolution:
    """Solve equality-constrained QP via a single dense linear solve."""
    P, q, A, b = problem.P, problem.q, problem.A, problem.b
    n = P.shape[0]
    m = A.shape[0]
    K = build_equality_kkt(P, A)
    rhs = np.concatenate([-q, b]) if m else -q.copy()
    try:
        sol = np.linalg.solve(K, rhs)
    except np.linalg.LinAlgError as exc:
        raise NumericalFailure(f"KKT solve failed: {exc}") from exc
    x = sol[:n]
    nu = sol[n:] if m else np.zeros(0)
    return EqualityKKTSolution(x=x, nu=nu)


def build_reduced_kkt_sparse(
    P: NDArray[np.float64],
    A: NDArray[np.float64],
    G: NDArray[np.float64],
    W: NDArray[np.float64],
) -> Any:
    """Return reduced KKT matrix [[P + G^T W G, A^T], [A, 0]] as CSC."""
    import scipy.sparse as sp

    m = A.shape[0]
    H = P + G.T @ (W[:, None] * G)
    H_sp = sp.csc_matrix(H)
    if m == 0:
        return H_sp
    A_sp = sp.csc_matrix(A)
    return sp.bmat([[H_sp, A_sp.T], [A_sp, None]], format="csc")
