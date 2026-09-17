"""Public result object for the QP solver."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass
class SolverResult:
    """Result of a QP solve."""

    status: str
    x: NDArray[np.float64]
    objective: float
    iterations: int
    primal_residual: float
    dual_residual: float
    duality_gap: float
    solve_time: float
    y: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    z: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    s: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    diagnostics: list[dict[str, float]] = field(default_factory=list)
