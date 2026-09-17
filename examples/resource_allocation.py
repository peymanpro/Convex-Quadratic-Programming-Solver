"""Resource allocation example."""

from __future__ import annotations

import numpy as np

from solver import QPProblem, solve


def main() -> None:
    # Minimize 0.5 x^T x - c^T x subject to sum(x) <= 1, x >= 0
    c = np.array([1.0, 2.0, 3.0])
    P = np.eye(3)
    q = -c
    A = np.zeros((0, 3))
    b = np.zeros(0)
    G = np.array(
        [
            [1.0, 1.0, 1.0],
            [-1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, -1.0],
        ]
    )
    h = np.array([1.0, 0.0, 0.0, 0.0])
    problem = QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)
    result = solve(problem)
    print("status =", result.status)
    print("allocation =", result.x)
    print("objective =", result.objective)


if __name__ == "__main__":
    main()
