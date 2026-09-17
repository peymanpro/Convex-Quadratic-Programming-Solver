"""Reference comparison: our solver vs OSQP on random convex QPs."""

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

    if osqp is None:
        return out

    try:
        m = osqp.OSQP()
        m.setup(
            P=sp.csc_matrix(prob.P),
            q=prob.q,
            A=sp.csc_matrix(np.vstack([prob.A, prob.G]))
            if prob.m
            else sp.csc_matrix(prob.G),
            l=np.concatenate([prob.b, -np.inf * np.ones(prob.p)])
            if prob.m
            else -np.inf * np.ones(prob.p),
            u=np.concatenate([prob.b, prob.h]) if prob.m else prob.h,
            verbose=False,
        )
        res = m.solve()
        out["osqp_status"] = 1.0 if res.info.status == "solved" else 0.0
        out["osqp_obj"] = float(res.info.obj_val)
        out["obj_diff"] = abs(r.objective - out["osqp_obj"])
        out["x_diff"] = float(np.max(np.abs(r.x - res.x)))
    except Exception as exc:  # noqa: BLE001
        out["osqp_error"] = 1.0
        out["osqp_msg"] = str(exc)[:80]

    return out


def main() -> int:
    rows = []
    for n, p in [(5, 3), (10, 5), (20, 10), (40, 20)]:
        rows.append(compare(n, p, seed=n))
    out = Path("benchmarks") / "results"
    out.mkdir(parents=True, exist_ok=True)
    (out / "reference_compare.json").write_text(json.dumps(rows, indent=2))
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
