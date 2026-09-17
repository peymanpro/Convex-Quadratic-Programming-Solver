"""Convex QP solver public interface."""

from __future__ import annotations

import time

from solver.exceptions import (
    DimensionMismatch,
    InfeasibleProblem,
    InvalidProblem,
    NonConvexProblem,
    NumericalFailure,
    QPError,
    UnboundedProblem,
)
from solver.ipm import IPMOptions, solve_ipm
from solver.mehrotra import solve_mehrotra
from solver.problem import QPProblem
from solver.result import SolverResult
from solver.validation import validate_problem

__version__ = "0.2.0"


def solve(
    problem: QPProblem,
    *,
    method: str = "mehrotra",
    options: IPMOptions | None = None,
    backend: str = "dense",
) -> SolverResult:
    """Solve a convex QP and return a SolverResult.

    Args:
        problem: QPProblem instance.
        method: "mehrotra" (default) or "ipm".
        options: IPMOptions; defaults used if None.
        backend: "dense" (default) or "sparse".

    Raises:
        InvalidProblem, NonConvexProblem, DimensionMismatch: bad data.
        ValueError: unknown method.
    """
    validate_problem(problem)
    if options is None:
        options = IPMOptions(backend=backend)
    elif backend != "dense":
        options = IPMOptions(
            max_iter=options.max_iter,
            tol=options.tol,
            mu0=options.mu0,
            sigma=options.sigma,
            eta=options.eta,
            regularization=options.regularization,
            backend=backend,
            sparse_threshold=options.sparse_threshold,
        )
    if method == "mehrotra":
        solver = solve_mehrotra
    elif method == "ipm":
        solver = solve_ipm
    else:
        raise ValueError(f"Unknown method: {method!r}")

    t0 = time.perf_counter()
    inner = solver(problem, options)
    elapsed = time.perf_counter() - t0

    return SolverResult(
        status=inner.status,
        x=inner.x,
        objective=inner.objective,
        iterations=inner.iterations,
        primal_residual=inner.primal_residual,
        dual_residual=inner.dual_residual,
        duality_gap=inner.duality_gap,
        solve_time=elapsed,
        y=inner.y,
        z=inner.z,
        s=inner.s,
        diagnostics=list(inner.history),
    )


__all__ = [
    "QPProblem",
    "SolverResult",
    "IPMOptions",
    "solve",
    "validate_problem",
    "QPError",
    "InvalidProblem",
    "NonConvexProblem",
    "DimensionMismatch",
    "NumericalFailure",
    "InfeasibleProblem",
    "UnboundedProblem",
    "__version__",
]
