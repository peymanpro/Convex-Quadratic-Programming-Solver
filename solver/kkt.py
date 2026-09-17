"""Equality-constrained KKT system and sparse KKT builders."""

from __future__ import annotations

from dataclasses import dataclass

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
