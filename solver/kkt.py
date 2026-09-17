"""Equality-constrained KKT system.

For:
    min  0.5 x^T P x + q^T x
    s.t. A x = b

The first-order (KKT) system is

    [ P  A^T ] [ x ]   [ -q ]
    [ A   0  ] [ v ] = [  b ]

This module assembles that system and solves it densely with
numpy.linalg.solve. Sparse support arrives in Phase 7.
"""

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
    """Assemble the (n+m, n+m) symmetric KKT matrix

        K = [[P, A^T],
             [A, 0  ]]

    Raises DimensionMismatch if shapes are incompatible.
    """
    n = P.shape[0]
    m = A.shape[0]
    K = np.zeros((n + m, n + m), dtype=np.float64)
    K[:n, :n] = P
    if m:
        K[:n, n:] = A.T
        K[n:, :n] = A
    return K


def solve_equality_qp(problem: QPProblem) -> EqualityKKTSolution:
    """Solve the equality-constrained QP via a single dense linear solve.

    Raises:
        NumericalFailure: the KKT matrix is singular or the solve fails.
    """
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
