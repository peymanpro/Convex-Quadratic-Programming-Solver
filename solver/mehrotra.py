"""Mehrotra predictor-corrector primal-dual IPM for convex QP."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from solver.ipm import IPMOptions, IPMResult, _solve_equality_only, _step_length
from solver.problem import QPProblem
from solver.residuals import compute_residuals


def _build_reduced_kkt(
    P: NDArray[np.float64],
    A: NDArray[np.float64],
    G: NDArray[np.float64],
    W: NDArray[np.float64],
    reg: float,
) -> NDArray[np.float64]:
    n = P.shape[0]
    m = A.shape[0]
    H = P + G.T @ (W[:, None] * G) + reg * np.eye(n)
    K = np.zeros((n + m, n + m), dtype=np.float64)
    K[:n, :n] = H
    if m:
        K[:n, n:] = A.T
        K[n:, :n] = A
    return K


def solve_mehrotra(
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
        mu = float(s @ z) / p

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
        if it == options.max_iter:
            break

        W = z / s
        K = _build_reduced_kkt(P, A, G, W, options.regularization)

        # --- Affine predictor ---
        r_c_aff = s * z
        bx_aff = -r_d + G.T @ (r_c_aff / s) - G.T @ (W * r_g)
        rhs_aff = np.concatenate([bx_aff, -r_p]) if m else bx_aff
        try:
            sol_aff = np.linalg.solve(K, rhs_aff)
        except np.linalg.LinAlgError:
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
        r_c_cor = s * z + ds_aff * dz_aff - sigma * mu * np.ones(p)
        bx_cor = -r_d + G.T @ (r_c_cor / s) - G.T @ (W * r_g)
        rhs_cor = np.concatenate([bx_cor, -r_p]) if m else bx_cor
        try:
            sol = np.linalg.solve(K, rhs_cor)
        except np.linalg.LinAlgError:
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
