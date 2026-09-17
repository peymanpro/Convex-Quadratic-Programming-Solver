"""Linear solver abstraction: dense vs sparse KKT systems."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import scipy.sparse as sp
from numpy.typing import NDArray
from scipy.sparse.linalg import splu

from solver.exceptions import NumericalFailure

Backend = Literal["dense", "sparse"]


@dataclass
class LinearSolverOptions:
    backend: Backend = "dense"
    sparse_threshold: int = 50  # auto: use sparse if dim >= threshold


def _auto_backend(dim: int, options: LinearSolverOptions) -> Backend:
    return "sparse" if dim >= options.sparse_threshold else options.backend


def dense_factor(
    K: NDArray[np.float64],
) -> tuple[NDArray[np.float64], None]:
    """Dense factor stub (no factorization; solve directly)."""
    return K, None


def sparse_factor(K: NDArray[np.float64]) -> sp.linalg.SuperLU:
    """Sparse LU factorization of K using SuperLU."""
    Ks = sp.csc_matrix(K)
    try:
        return splu(Ks)
    except RuntimeError as exc:
        raise NumericalFailure(f"Sparse LU failed: {exc}") from exc


def solve_dense(
    K: NDArray[np.float64], rhs: NDArray[np.float64]
) -> NDArray[np.float64]:
    try:
        return np.linalg.solve(K, rhs)
    except np.linalg.LinAlgError as exc:
        raise NumericalFailure(f"Dense solve failed: {exc}") from exc


def solve_sparse(
    lu: sp.linalg.SuperLU,
    rhs: NDArray[np.float64],
) -> NDArray[np.float64]:
    result = lu.solve(rhs)
    return np.asarray(result, dtype=np.float64)


def factor_and_solve(
    K: NDArray[np.float64],
    rhs: NDArray[np.float64],
    options: LinearSolverOptions | None = None,
) -> NDArray[np.float64]:
    """Factor K and solve K x = rhs, dispatching on backend."""
    if options is None:
        options = LinearSolverOptions()
    backend = _auto_backend(K.shape[0], options)
    if backend == "sparse":
        lu = sparse_factor(K)
        return solve_sparse(lu, rhs)
    return solve_dense(K, rhs)
