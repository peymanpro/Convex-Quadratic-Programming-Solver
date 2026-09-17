"""Reference comparison: our solver vs OSQP and Clarabel."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import scipy.sparse as sp

from benchmarks.run import make_qp
from solver import solve

try:
    import osqp  # type: ignore
except ImportError:
    osqp = None

try:
    import clarabel  # type: ignore
except ImportError:
    clarabel = None


def _compare_osqp(
    prob: Any, out: dict[str, Any], our_obj: float, our_x: np.ndarray
) -> None:
    if osqp is None:
        return
    try:
        m = osqp.OSQP()
        A = (
            sp.csc_matrix(np.vstack([prob.A, prob.G]))
            if prob.m
            else sp.csc_matrix(prob.G)
        )
        lower = (
            np.concatenate([prob.b, -np.inf * np.ones(prob.p)])
            if prob.m
            else -np.inf * np.ones(prob.p)
        )
        u = np.concatenate([prob.b, prob.h]) if prob.m else prob.h
        m.setup(P=sp.csc_matrix(prob.P), q=prob.q, A=A, l=lower, u=u, verbose=False)
        res = m.solve()
        out["osqp_status"] = 1.0 if res.info.status == "solved" else 0.0
        out["osqp_obj"] = float(res.info.obj_val)
        out["osqp_obj_diff"] = abs(our_obj - float(res.info.obj_val))
        out["osqp_x_diff"] = float(np.max(np.abs(our_x - res.x)))
    except Exception as exc:  # noqa: BLE001
        out["osqp_error"] = 1.0
        out["osqp_msg"] = str(exc)[:120]


def _compare_clarabel(
    prob: Any, out: dict[str, Any], our_obj: float, our_x: np.ndarray
) -> None:
    if clarabel is None:
        return
    try:
        if prob.m:
            A_c = sp.csc_matrix(np.vstack([prob.G, prob.A]))
            b_c = np.concatenate([prob.h, prob.b])
        else:
            A_c = sp.csc_matrix(prob.G)
            b_c = prob.h
        cones = [clarabel.NonnegativeConeT(prob.p)]
        if prob.m:
            cones.append(clarabel.ZeroConeT(prob.m))
        settings = clarabel.DefaultSettings()
        settings.verbose = False
        solver = clarabel.DefaultSolver(
            sp.csc_matrix(prob.P), prob.q, A_c, b_c, cones, settings
        )
        res = solver.solve()
        out["clarabel_status"] = str(res.status)
        out["clarabel_obj"] = float(res.obj_val)
        out["clarabel_obj_diff"] = abs(our_obj - float(res.obj_val))
        out["clarabel_x_diff"] = float(np.max(np.abs(our_x - np.asarray(res.x))))
    except Exception as exc:  # noqa: BLE001
        out["clarabel_error"] = 1.0
        out["clarabel_msg"] = str(exc)[:120]


def compare(n: int, p: int, seed: int) -> dict[str, Any]:
    prob = make_qp(n, p, seed)
    r = solve(prob)
    out: dict[str, Any] = {
        "n": float(n),
        "p": float(p),
        "our_status": 1.0 if r.status == "optimal" else 0.0,
        "our_obj": r.objective,
        "our_iters": float(r.iterations),
    }
    _compare_osqp(prob, out, r.objective, r.x)
    _compare_clarabel(prob, out, r.objective, r.x)
    return out


def main() -> int:
    rows = []
    for n, p in [(5, 3), (10, 5), (20, 10), (40, 20)]:
        rows.append(compare(n, p, seed=n))
    out_dir = Path("benchmarks") / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "reference_compare.json").write_text(
        json.dumps(rows, indent=2, default=str)
    )
    print(json.dumps(rows, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
