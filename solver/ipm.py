"""Primal-dual interior-point method for convex QP."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from solver.linear_solver import (
    LinearSolverOptions,
    assemble_kkt,
    factor_and_solve,
)
from solver.problem import QPProblem
from solver.residuals import compute_residuals


@dataclass
class IPMOptions:
    max_iter: int = 200
    tol: float = 1e-8
    mu0: float = 1.0
    sigma: float = 0.1
    eta: float = 0.995
    regularization: float = 1e-10
    backend: str = "dense"  # "dense" or "sparse"
    sparse_threshold: int = 100_000


@dataclass
class IPMResult:
    x: NDArray[np.float64]
    y: NDArray[np.float64]
    z: NDArray[np.float64]
    s: NDArray[np.float64]
    status: str
    iterations: int
    objective: float
    primal_residual: float
    dual_residual: float
    duality_gap: float
    history: list[dict[str, float]] = field(default_factory=list)


def _step_length(
    v: NDArray[np.float64],
    dv: NDArray[np.float64],
    eta: float,
) -> float:
    """Fraction-to-boundary step keeping v + alpha*dv >= 0."""
    neg = dv < 0
    if not np.any(neg):
        return 1.0
    return float(min(1.0, eta * np.min(-v[neg] / dv[neg])))


def _solve_equality_only(
    P: NDArray[np.float64],
    q: NDArray[np.float64],
    A: NDArray[np.float64],
    b: NDArray[np.float64],
    p: int,
) -> IPMResult:
    n = P.shape[0]
    m = A.shape[0]
    K = np.zeros((n + m, n + m), dtype=np.float64)
    K[:n, :n] = P
    if m:
        K[:n, n:] = A.T
        K[n:, :n] = A
        rhs = np.concatenate([-q, b])
    else:
        rhs = -q.copy()
    sol = np.linalg.solve(K, rhs)
    x = sol[:n]
    y = sol[n:] if m else np.zeros(0)
    z = np.zeros(p)
    s = np.zeros(p)
    res = compute_residuals(P, q, A, b, np.zeros((0, n)), np.zeros(0), x, y, z)
    obj = float(0.5 * x @ P @ x + q @ x)
    return IPMResult(
        x=x,
        y=y,
        z=z,
        s=s,
        status="optimal",
        iterations=0,
        objective=obj,
        primal_residual=res.primal,
        dual_residual=res.stationarity,
        duality_gap=0.0,
        history=[],
    )


def _solve_ipm_impl(
    problem: QPProblem,
    options: IPMOptions | None = None,
) -> IPMResult:
    """Solve a convex QP via primal-dual interior-point method."""
    if options is None:
        options = IPMOptions()

    P, q, A, b, G, h = (
        problem.P,
        problem.q,
        problem.A,
        problem.b,
        problem.G,
        problem.h,
    )
    n = problem.n
    m = problem.m
    p = problem.p

    if p == 0:
        return _solve_equality_only(P, q, A, b, p)

    # --- Initialization ---
    x = np.zeros(n, dtype=np.float64)
    if m:
        x = np.linalg.lstsq(A, b, rcond=None)[0]
    y = np.zeros(m, dtype=np.float64)
    s = np.ones(p, dtype=np.float64)
    z = np.ones(p, dtype=np.float64)

    history: list[dict[str, float]] = []
    status = "max_iter"
    it = 0

    for it in range(options.max_iter + 1):
        r_d = P @ x + q
        if m:
            r_d = r_d + A.T @ y
        r_d = r_d + G.T @ z
        r_p = A @ x - b if m else np.zeros(0)
        r_g = G @ x + s - h
        if not (
            np.all(np.isfinite(x))
            and np.all(np.isfinite(s))
            and np.all(np.isfinite(z))
            and np.all(np.isfinite(r_d))
            and np.all(np.isfinite(r_g))
        ):
            status = "numerical_failure"
            break
        if float(np.max(np.abs(x))) > 1e10:
            status = "unbounded"
            break
        mu = float(s @ z) / p
        if mu < 0 or not np.isfinite(mu):
            status = "numerical_failure"
            break
        r_c = s * z - options.sigma * mu * np.ones(p)

        res = compute_residuals(P, q, A, b, G, h, x, y, z)
        history.append(
            {
                "iter": float(it),
                "objective": float(0.5 * x @ P @ x + q @ x),
                "primal_residual": res.primal,
                "dual_residual": res.stationarity,
                "duality_gap": float(s @ z),
                "mu": mu,
            }
        )

        if (
            res.primal <= options.tol
            and res.stationarity <= options.tol
            and float(s @ z) <= options.tol
        ):
            status = "optimal"
            break
        if it > 5 and (
            (res.primal > 1e3 and res.stationarity < 1e-6)
            or (
                res.primal > 0.5
                and res.stationarity > 0.5
                and it >= 15
                and len(history) >= 5
                and history[-1]["primal_residual"]
                >= 0.9 * history[-5]["primal_residual"]
            )
        ):
            status = "infeasible"
            break
        if it == options.max_iter:
            break

        W = z / s
        K = assemble_kkt(
            P,
            A,
            G,
            W,
            options.regularization,
            backend=options.backend,  # type: ignore[arg-type]
        )

        bx = -r_d + G.T @ (r_c / s) - G.T @ (W * r_g)
        rhs = np.concatenate([bx, -r_p]) if m else bx

        try:
            sol = factor_and_solve(
                K,
                rhs,
                LinearSolverOptions(
                    backend=options.backend,  # type: ignore[arg-type]
                    sparse_threshold=options.sparse_threshold,
                ),
            )
        except Exception:
            status = "numerical_failure"
            break
        dx = sol[:n]
        dy = sol[n:] if m else np.zeros(0)
        ds = -r_g - G @ dx
        dz = (-r_c - z * ds) / s

        alpha_p = _step_length(s, ds, options.eta)
        alpha_d = _step_length(z, dz, options.eta)
        alpha = min(alpha_p, alpha_d)

        history[-1]["step_length"] = float(alpha)
        x = x + alpha * dx
        if m:
            y = y + alpha * dy
        s = s + alpha * ds
        z = z + alpha * dz

    obj = float(0.5 * x @ P @ x + q @ x)
    res = compute_residuals(P, q, A, b, G, h, x, y, z)

    return IPMResult(
        x=x,
        y=y,
        z=z,
        s=s,
        status=status,
        iterations=it,
        objective=obj,
        primal_residual=res.primal,
        dual_residual=res.stationarity,
        duality_gap=float(s @ z),
        history=history,
    )


def solve_ipm(
    problem: QPProblem,
    options: IPMOptions | None = None,
) -> IPMResult:
    """Wrapper suppressing floating-point warnings during divergence."""
    old = np.seterr(invalid="ignore", divide="ignore", over="ignore")
    try:
        return _solve_ipm_impl(problem, options)
    finally:
        np.seterr(**old)
