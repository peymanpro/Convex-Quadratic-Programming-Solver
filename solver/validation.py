"""Validation of QP problem data: shape, convexity, finiteness."""

from __future__ import annotations

import numpy as np

from solver.exceptions import (
    DimensionMismatch,
    InvalidProblem,
    NonConvexProblem,
)
from solver.problem import QPProblem

SYM_TOL = 1e-10
PSD_TOL = 1e-10


def _check_finite(name: str, arr: np.ndarray) -> None:
    if not np.all(np.isfinite(arr)):
        raise InvalidProblem(f"{name} contains NaN or Inf.")


def validate_problem(problem: QPProblem) -> None:
    """Validate shapes, finiteness, and convexity.

    Raises:
        InvalidProblem: malformed data or non-finite values.
        DimensionMismatch: inconsistent array shapes.
        NonConvexProblem: P is not symmetric positive semidefinite.
    """
    P, q, A, b, G, h = (
        problem.P,
        problem.q,
        problem.A,
        problem.b,
        problem.G,
        problem.h,
    )

    for name, arr in (
        ("P", P),
        ("q", q),
        ("A", A),
        ("b", b),
        ("G", G),
        ("h", h),
    ):
        if not isinstance(arr, np.ndarray):
            raise InvalidProblem(f"{name} must be a numpy.ndarray.")
        _check_finite(name, arr)

    if P.ndim != 2 or P.shape[0] != P.shape[1]:
        raise DimensionMismatch("P must be square (n, n).")
    n = P.shape[0]

    if q.shape != (n,):
        raise DimensionMismatch(f"q must have shape ({n},), got {q.shape}.")
    if A.ndim != 2 or A.shape[1] != n:
        raise DimensionMismatch(f"A must have shape (m, {n}), got {A.shape}.")
    if b.shape != (A.shape[0],):
        raise DimensionMismatch(f"b must have shape ({A.shape[0]},), got {b.shape}.")
    if G.ndim != 2 or G.shape[1] != n:
        raise DimensionMismatch(f"G must have shape (p, {n}), got {G.shape}.")
    if h.shape != (G.shape[0],):
        raise DimensionMismatch(f"h must have shape ({G.shape[0]},), got {h.shape}.")

    asym = np.max(np.abs(P - P.T)) if P.size else 0.0
    scale = max(1.0, float(np.max(np.abs(P))) if P.size else 1.0)
    if asym / scale > SYM_TOL:
        raise NonConvexProblem("P is not symmetric within tolerance.")

    if P.size:
        Psym = 0.5 * (P + P.T)
        eigs = np.linalg.eigvalsh(Psym)
        if eigs.size and float(eigs[0]) < -PSD_TOL * max(1.0, float(eigs[-1])):
            raise NonConvexProblem(
                f"P is not positive semidefinite (min eig = {eigs[0]:.3e})."
            )
