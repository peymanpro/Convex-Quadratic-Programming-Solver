"""Typed representation of a convex quadratic program."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class QPProblem:
    """Standard convex QP:

        min  0.5 x^T P x + q^T x
        s.t. A x = b
             G x <= h

    Attributes:
        P: symmetric positive semidefinite (n, n).
        q: linear cost (n,).
        A: equality matrix (m, n). Use shape (0, n) if no equalities.
        b: equality rhs (m,). Use shape (0,) if no equalities.
        G: inequality matrix (p, n). Use shape (0, n) if no inequalities.
        h: inequality rhs (p,). Use shape (0,) if no inequalities.
    """

    P: NDArray[np.float64]
    q: NDArray[np.float64]
    A: NDArray[np.float64]
    b: NDArray[np.float64]
    G: NDArray[np.float64]
    h: NDArray[np.float64]

    @property
    def n(self) -> int:
        return int(self.P.shape[0])

    @property
    def m(self) -> int:
        return int(self.A.shape[0])

    @property
    def p(self) -> int:
        return int(self.G.shape[0])
