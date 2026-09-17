"""Solver adapter: converts API payloads to QPProblem and back."""

from __future__ import annotations

from typing import Any

import numpy as np

from solver import IPMOptions, QPProblem, solve


def _as_2d(rows: list[list[float]], n_cols: int) -> np.ndarray:
    if not rows:
        return np.zeros((0, n_cols))
    return np.asarray(rows, dtype=np.float64)


def _as_1d(rows: list[float]) -> np.ndarray:
    if not rows:
        return np.zeros(0)
    return np.asarray(rows, dtype=np.float64)


def payload_to_problem(data: dict[str, Any]) -> QPProblem:
    P = np.asarray(data["P"], dtype=np.float64)
    q = np.asarray(data["q"], dtype=np.float64)
    n = q.shape[0]
    A = _as_2d(data.get("A", []), n)
    b = _as_1d(data.get("b", []))
    G = _as_2d(data.get("G", []), n)
    h = _as_1d(data.get("h", []))
    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)


def solve_from_payload(data: dict[str, Any]) -> dict[str, Any]:
    problem = payload_to_problem(data)
    options = IPMOptions(
        tol=float(data.get("tol", 1e-8)),
        max_iter=int(data.get("max_iter", 200)),
    )
    result = solve(
        problem,
        method=str(data.get("method", "mehrotra")),
        options=options,
    )
    return {
        "status": result.status,
        "x": result.x.tolist(),
        "objective": result.objective,
        "iterations": result.iterations,
        "primal_residual": result.primal_residual,
        "dual_residual": result.dual_residual,
        "duality_gap": result.duality_gap,
        "solve_time": result.solve_time,
    }
