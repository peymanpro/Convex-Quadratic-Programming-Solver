"""Portfolio optimization example."""

from __future__ import annotations

import numpy as np

from solver import QPProblem, solve


def main() -> None:
    # Minimize variance x^T S x subject to sum(x) = 1, x >= 0
    S = np.array([[0.04, 0.01], [0.01, 0.09]])
    P = 2.0 * S
    q = np.zeros(2)
    A = np.array([[1.0, 1.0]])
    b = np.array([1.0])
    G = np.array([[-1.0, 0.0], [0.0, -1.0]])
    h = np.array([0.0, 0.0])
    problem = QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)
    result = solve(problem)
    print("status =", result.status)
    print("weights =", result.x)
    print("objective =", result.objective)


if __name__ == "__main__":
    main()
