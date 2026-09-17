"""Mehrotra predictor-corrector primal-dual IPM for convex QP."""

from __future__ import annotations

import numpy as np

from solver.ipm import IPMOptions, IPMResult, _solve_equality_only, _step_length
from solver.linear_solver import (
    LinearSolverOptions,
    assemble_kkt,
    factor_and_solve,
)
from solver.problem import QPProblem
from solver.residuals import compute_residuals


def _solve_mehrotra_impl(
    problem: QPProblem,
    options: IPMOptions | None = None,
) -> IPMResult:
    """Solve convex QP via Mehrotra predictor-corrector IPM."""
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
    n, m, p = problem.n, problem.m, problem.p

    if p == 0:
        return _solve_equality_only(P, q, A, b, p)

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
        if (
            mu < 0
            or not np.isfinite(mu)
            or float(np.min(s)) <= 1e-300
            or float(np.min(z)) <= 1e-300
        ):
            status = "numerical_failure"
            break

        res = compute_residuals(P, q, A, b, G, h, x, y, z)
        history.append(
            {
                "iter": float(it),
                "objective": float(0.5 * x @ P @ x + q @ x),
                "primal_residual": res.primal,
                "dual_residual": res.stationarity,
                "duality_gap": float(s @ z),
                "mu": mu,
                "sigma": 0.0,
                "step_length": 0.0,
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

        # --- Affine predictor ---
        r_c_aff = s * z
        bx_aff = -r_d + G.T @ (r_c_aff / s) - G.T @ (W * r_g)
        rhs_aff = np.concatenate([bx_aff, -r_p]) if m else bx_aff
        try:
            sol_aff = factor_and_solve(
                K,
                rhs_aff,
                LinearSolverOptions(
                    backend=options.backend,  # type: ignore[arg-type]
                    sparse_threshold=options.sparse_threshold,
                ),
            )
        except Exception:
            status = "numerical_failure"
            break
        dx_aff = sol_aff[:n]
        ds_aff = -r_g - G @ dx_aff
        dz_aff = (-r_c_aff - z * ds_aff) / s

        alpha_aff_p = _step_length(s, ds_aff, options.eta)
        alpha_aff_d = _step_length(z, dz_aff, options.eta)

        s_aff = s + alpha_aff_p * ds_aff
        z_aff = z + alpha_aff_d * dz_aff
        mu_aff = float(s_aff @ z_aff) / p
        sigma = float(min(1.0, max(0.0, (mu_aff / mu) ** 3))) if mu > 0 else 0.0

        # --- Corrector ---
        if not (
            np.all(np.isfinite(s_aff))
            and np.all(np.isfinite(z_aff))
            and np.isfinite(mu_aff)
            and np.isfinite(sigma)
        ):
            status = "numerical_failure"
            break
        r_c_cor = s * z + ds_aff * dz_aff - sigma * mu * np.ones(p)
        bx_cor = -r_d + G.T @ (r_c_cor / s) - G.T @ (W * r_g)
        rhs_cor = np.concatenate([bx_cor, -r_p]) if m else bx_cor
        try:
            sol = factor_and_solve(
                K,
                rhs_cor,
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
        dz = (-r_c_cor - z * ds) / s

        alpha_p = _step_length(s, ds, options.eta)
        alpha_d = _step_length(z, dz, options.eta)
        alpha = min(alpha_p, alpha_d)

        history[-1]["sigma"] = float(sigma)
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


def solve_mehrotra(
    problem: QPProblem,
    options: IPMOptions | None = None,
) -> IPMResult:
    """Wrapper suppressing floating-point warnings during divergence."""
    old = np.seterr(invalid="ignore", divide="ignore", over="ignore")
    try:
        return _solve_mehrotra_impl(problem, options)
    finally:
        np.seterr(**old)
