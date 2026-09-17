"""Command-line interface for the convex QP solver."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from solver import QPProblem, __version__, solve


def _load_problem(path: Path) -> QPProblem:
    data = json.loads(path.read_text())
    P = np.asarray(data["P"], dtype=np.float64)
    q = np.asarray(data["q"], dtype=np.float64)
    n = q.shape[0]
    A = np.asarray(data.get("A", []), dtype=np.float64).reshape(-1, n)
    b = np.asarray(data.get("b", []), dtype=np.float64)
    G = np.asarray(data.get("G", []), dtype=np.float64).reshape(-1, n)
    h = np.asarray(data.get("h", []), dtype=np.float64)
    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cqp-solve",
        description="Solve a convex QP from a JSON file.",
    )
    parser.add_argument("input", type=Path, help="Path to QP JSON file.")
    parser.add_argument("--method", choices=["mehrotra", "ipm"], default="mehrotra")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)

    problem = _load_problem(args.input)
    result = solve(problem, method=args.method)
    print(
        json.dumps(
            {
                "status": result.status,
                "x": result.x.tolist(),
                "objective": result.objective,
                "iterations": result.iterations,
                "primal_residual": result.primal_residual,
                "dual_residual": result.dual_residual,
                "duality_gap": result.duality_gap,
                "solve_time": result.solve_time,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
