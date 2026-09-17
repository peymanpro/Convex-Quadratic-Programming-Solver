"""Three analytical convex QP examples with explicit KKT checks.

Each example provides data (P, q, A, b, G, h) and a closed-form optimal
solution (x*, nu*, lam*).  The script verifies that the candidate solution
satisfies the KKT system to a tight numerical tolerance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

TOL = 1e-10


@dataclass
class Example:
    name: str
    P: np.ndarray
    q: np.ndarray
    A: np.ndarray
    b: np.ndarray
    G: np.ndarray
    h: np.ndarray
    x: np.ndarray
    nu: np.ndarray
    lam: np.ndarray


def example_1_unconstrained() -> Example:
    """min 0.5 x^T P x + q^T x with P = I, q = -[1, 2].

    Closed form: x* = -P^{-1} q = [1, 2], nu = [], lam = [].
    """
    P = np.eye(2)
    q = np.array([-1.0, -2.0])
    A = np.zeros((0, 2))
    b = np.zeros(0)
    G = np.zeros((0, 2))
    h = np.zeros(0)
    x = np.array([1.0, 2.0])
    nu = np.zeros(0)
    lam = np.zeros(0)
    return Example("unconstrained_2d", P, q, A, b, G, h, x, nu, lam)


def example_2_equality() -> Example:
    """min 0.5 x^T P x + q^T x s.t. x1 + x2 = 1, P = I, q = 0.

    KKT: x + A^T nu = 0, A x = b.
    Solve: x = -A^T nu = -[nu, nu]; constraint nu = -1/2, x = [1/2, 1/2].
    """
    P = np.eye(2)
    q = np.zeros(2)
    A = np.array([[1.0, 1.0]])
    b = np.array([1.0])
    G = np.zeros((0, 2))
    h = np.zeros(0)
    x = np.array([0.5, 0.5])
    nu = np.array([-0.5])
    lam = np.zeros(0)
    return Example("equality_line_2d", P, q, A, b, G, h, x, nu, lam)


def example_3_inequality() -> Example:
    """min 0.5 (x1 - 2)^2 + 0.5 (x2 - 3)^2 s.t. x1 + x2 <= 2.

    Equivalent QP: P = I, q = -[2, 3], G = [[1, 1]], h = [2].
    Active constraint at optimum: x1 + x2 = 2.
    KKT: x - [2, 3] + lam * [1, 1] = 0  =>  x = [2 - lam, 3 - lam].
    Sum constraint: 5 - 2 lam = 2  =>  lam = 1.5, x = [0.5, 1.5].
    """
    P = np.eye(2)
    q = np.array([-2.0, -3.0])
    A = np.zeros((0, 2))
    b = np.zeros(0)
    G = np.array([[1.0, 1.0]])
    h = np.array([2.0])
    x = np.array([0.5, 1.5])
    nu = np.zeros(0)
    lam = np.array([1.5])
    return Example("inequality_halfplane_2d", P, q, A, b, G, h, x, nu, lam)


def kkt_residuals(ex: Example) -> dict[str, float]:
    r_d = ex.P @ ex.x + ex.q + ex.A.T @ ex.nu + ex.G.T @ ex.lam
    r_p_eq = ex.A @ ex.x - ex.b if ex.A.size else np.zeros(0)
    r_p_iq = np.maximum(0.0, ex.G @ ex.x - ex.h) if ex.G.size else np.zeros(0)
    r_c = float(ex.lam @ (ex.h - ex.G @ ex.x)) if ex.G.size else 0.0
    return {
        "stationarity": float(np.max(np.abs(r_d)) if r_d.size else 0.0),
        "primal_eq": float(np.max(np.abs(r_p_eq)) if r_p_eq.size else 0.0),
        "primal_iq": float(np.max(r_p_iq) if r_p_iq.size else 0.0),
        "complementarity": abs(r_c),
    }


def main() -> int:
    examples = [
        example_1_unconstrained(),
        example_2_equality(),
        example_3_inequality(),
    ]
    ok = True
    for ex in examples:
        res = kkt_residuals(ex)
        worst = max(res.values())
        status = "PASS" if worst <= TOL else "FAIL"
        print(f"{ex.name:28s} worst KKT residual = {worst:.2e}  [{status}]")
        if worst > TOL:
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
