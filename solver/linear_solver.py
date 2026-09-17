"""Linear solver abstraction: dense vs sparse KKT systems."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import scipy.sparse as sp
from numpy.typing import NDArray
from scipy.sparse.linalg import splu

from solver.exceptions import NumericalFailure

Backend = Literal["dense", "sparse"]
KKTMatrix = Any


@dataclass
class LinearSolverOptions:
    backend: Backend = "dense"
    sparse_threshold: int = 50_000


def _auto_backend(dim: int, options: LinearSolverOptions) -> Backend:
    if options.backend == "sparse":
        return "sparse"
    return "dense"


def assemble_kkt(
    P: NDArray[np.float64],
    A: NDArray[np.float64],
    G: NDArray[np.float64],
    W: NDArray[np.float64],
    reg: float,
    backend: Backend = "dense",
) -> KKTMatrix:
    """Assemble the reduced KKT matrix [[H, A^T], [A, 0]] as
    dense (ndarray) or sparse (CSC) depending on backend.

    Dense: H = P + G^T W G as ndarray, full (n+m) x (n+m) array.
    Sparse: H assembled via sparse matrix products; the (n+m) KKT is
    built with scipy.sparse.bmat without materializing a dense matrix.
    """
    n = P.shape[0]
    m = A.shape[0]

    if backend == "sparse":
        P_sp = sp.csc_matrix(P)
        G_sp = sp.csc_matrix(G)
        W_sp = sp.diags(W)
        H_sp = P_sp + G_sp.T @ W_sp @ G_sp + reg * sp.identity(n, format="csc")
        if m:
            A_sp = sp.csc_matrix(A)
            K_sp = sp.bmat([[H_sp, A_sp.T], [A_sp, None]], format="csc")
            return K_sp
        return H_sp

    H = P + G.T @ (W[:, None] * G) + reg * np.eye(n)
    K = np.zeros((n + m, n + m), dtype=np.float64)
    K[:n, :n] = H
    if m:
        K[:n, n:] = A.T
        K[n:, :n] = A
    return K


def sparse_factor(K: KKTMatrix) -> sp.linalg.SuperLU:
    """Sparse LU factorization via SuperLU."""
    Ks = K if sp.issparse(K) else sp.csc_matrix(K)
    try:
        return splu(Ks)
    except RuntimeError as exc:
        raise NumericalFailure(f"Sparse LU failed: {exc}") from exc


def solve_dense(K: KKTMatrix, rhs: NDArray[np.float64]) -> NDArray[np.float64]:
    if sp.issparse(K):
        Kd = np.asarray(K.todense(), dtype=np.float64)
    else:
        Kd = np.asarray(K, dtype=np.float64)
    try:
        return np.linalg.solve(Kd, rhs)
    except np.linalg.LinAlgError as exc:
        raise NumericalFailure(f"Dense solve failed: {exc}") from exc


def solve_sparse(
    lu: sp.linalg.SuperLU,
    rhs: NDArray[np.float64],
) -> NDArray[np.float64]:
    result = lu.solve(rhs)
    return np.asarray(result, dtype=np.float64)


def factor_and_solve(
    K: KKTMatrix,
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
