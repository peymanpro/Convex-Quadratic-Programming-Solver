"""Benchmark harness for the convex QP solver.

Reproducible: uses fixed seeds; records environment metadata.
"""

from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from solver import QPProblem, solve


def env_metadata() -> dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor(),
        "numpy": np.__version__,
    }


def make_qp(n: int, p: int, seed: int, cond: float = 10.0) -> QPProblem:
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    eigs = np.logspace(0.0, np.log10(cond), n)
    P = (Q * eigs) @ Q.T
    q = rng.standard_normal(n)
    x0 = rng.standard_normal(n)
    G = rng.standard_normal((p, n))
    h = G @ x0 + rng.uniform(0.5, 2.0, size=p)
    return QPProblem(
        P=P,
        q=q,
        A=np.zeros((0, n)),
        b=np.zeros(0),
        G=G,
        h=h,
    )


def _run_once(prob: QPProblem, method: str, backend: str) -> dict[str, Any]:
    t0 = time.perf_counter()
    r = solve(prob, method=method, backend=backend)
    elapsed = time.perf_counter() - t0
    return {
        "backend": backend,
        "method": method,
        "status_ok": 1.0 if r.status == "optimal" else 0.0,
        "iterations": float(r.iterations),
        "runtime_s": elapsed,
        "primal_residual": r.primal_residual,
        "dual_residual": r.dual_residual,
        "duality_gap": r.duality_gap,
        "objective": r.objective,
    }


def bench_sizes(
    sizes: list[int],
    method: str = "mehrotra",
    seed: int = 0,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in sizes:
        p = max(1, n // 2)
        prob = make_qp(n, p, seed)
        for backend in ("dense", "sparse"):
            row = _run_once(prob, method, backend)
            row["n"] = float(n)
            row["p"] = float(p)
            rows.append(row)
    return rows


def main() -> int:
    sizes = [10, 20, 40, 80, 160]
    meta = env_metadata()
    rows_meh = bench_sizes(sizes, method="mehrotra")
    rows_ipm = bench_sizes(sizes, method="ipm")
    out = Path("benchmarks") / "results"
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "env": meta,
        "sizes": sizes,
        "mehrotra": rows_meh,
        "ipm": rows_ipm,
    }
    (out / "size_scaling.json").write_text(json.dumps(payload, indent=2, default=str))
    print(json.dumps(payload, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
