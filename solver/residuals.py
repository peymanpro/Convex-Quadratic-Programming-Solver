"""KKT residual computation for convex QP.

Definitions used throughout the solver:

    r_d = P x + q + A^T nu + G^T lam      (stationarity)
    r_p = A x - b                          (primal equality)
    r_g = max(0, G x - h)                  (primal inequality)
    r_c = lam^T (h - G x)                  (complementarity)

All norms returned by this module are infinity norms for vectors,
and the complementarity value is a scalar.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class KKTResiduals:
    """Aggregated KKT residuals."""

    stationarity: float
    primal_eq: float
    primal_iq: float
    complementarity: float

    @property
    def primal(self) -> float:
        return max(self.primal_eq, self.primal_iq)

    @property
    def worst(self) -> float:
        return max(self.stationarity, self.primal, self.complementarity)


def compute_residuals(
    P: NDArray[np.float64],
    q: NDArray[np.float64],
    A: NDArray[np.float64],
    b: NDArray[np.float64],
    G: NDArray[np.float64],
    h: NDArray[np.float64],
    x: NDArray[np.float64],
    nu: NDArray[np.float64],
    lam: NDArray[np.float64],
) -> KKTResiduals:
    """Compute KKT residuals for a candidate (x, nu, lam)."""
    r_d = P @ x + q
    if A.shape[0]:
        r_d = r_d + A.T @ nu
    if G.shape[0]:
        r_d = r_d + G.T @ lam

    r_p_eq = A @ x - b if A.shape[0] else np.zeros(0)
    r_p_iq = np.maximum(0.0, G @ x - h) if G.shape[0] else np.zeros(0)
    r_c = float(lam @ (h - G @ x)) if G.shape[0] else 0.0

    return KKTResiduals(
        stationarity=float(np.max(np.abs(r_d))) if r_d.size else 0.0,
        primal_eq=float(np.max(np.abs(r_p_eq))) if r_p_eq.size else 0.0,
        primal_iq=float(np.max(r_p_iq)) if r_p_iq.size else 0.0,
        complementarity=abs(r_c),
    )
