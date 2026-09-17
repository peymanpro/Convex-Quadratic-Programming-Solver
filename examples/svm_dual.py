"""Support vector machine dual QP example (simplified)."""

from __future__ import annotations

import numpy as np

from solver import QPProblem, solve


def main() -> None:
    # Minimal SVM dual: min 0.5 a^T Q a - 1^T a  s.t. y^T a = 0, 0 <= a <= C
    y = np.array([1.0, -1.0, 1.0])
    C = 1.0
    Q = np.outer(y, y) + 1e-3 * np.eye(3)
    P = Q
    q = -np.ones(3)
    A = y.reshape(1, 3)
    b = np.array([0.0])
    G = np.vstack([np.eye(3), -np.eye(3)])
    h = np.concatenate([C * np.ones(3), np.zeros(3)])
    problem = QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)
    result = solve(problem)
    print("status =", result.status)
    print("alpha =", result.x)
    print("objective =", result.objective)


if __name__ == "__main__":
    main()
