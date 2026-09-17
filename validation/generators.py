"""Random convex QP generators for the validation corpus."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from solver.problem import QPProblem


def random_psd(
    n: int,
    rng: np.random.Generator,
    cond: float = 10.0,
) -> NDArray[np.float64]:
    """Random symmetric positive definite matrix with given condition."""
    Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    eigs = np.logspace(0.0, np.log10(cond), n)
    return (Q * eigs) @ Q.T


def random_feasible_qp(
    n: int,
    p: int,
    rng: np.random.Generator,
    cond: float = 10.0,
) -> QPProblem:
    """Random convex QP with a known strictly feasible interior point."""
    P = random_psd(n, rng, cond)
    q = rng.standard_normal(n)
    A = np.zeros((0, n))
    b = np.zeros(0)

    x0 = rng.standard_normal(n)
    G = rng.standard_normal((p, n))
    slack = rng.uniform(0.5, 2.0, size=p)
    h = G @ x0 + slack  # x0 strictly feasible

    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)


def random_mixed_qp(
    n: int,
    m: int,
    p: int,
    rng: np.random.Generator,
    cond: float = 10.0,
) -> QPProblem:
    """Random convex QP with both equality and inequality constraints."""
    P = random_psd(n, rng, cond)
    q = rng.standard_normal(n)

    if m > 0:
        x0 = rng.standard_normal(n)
        A = rng.standard_normal((m, n))
        b = A @ x0
    else:
        A = np.zeros((0, n))
        b = np.zeros(0)
        x0 = rng.standard_normal(n)

    G = rng.standard_normal((p, n))
    slack = rng.uniform(0.5, 2.0, size=p)
    h = G @ x0 + slack

    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)


def ill_conditioned_qp(
    n: int,
    cond: float,
    rng: np.random.Generator,
) -> QPProblem:
    """Random convex QP with P having the requested condition number."""
    return random_feasible_qp(n, n, rng, cond=cond)


def infeasible_qp(rng: np.random.Generator) -> QPProblem:
    """Contradictory inequalities: x <= -1 and -x <= -1."""
    _ = rng
    P = np.eye(1)
    q = np.zeros(1)
    A = np.zeros((0, 1))
    b = np.zeros(0)
    G = np.array([[1.0], [-1.0]])
    h = np.array([-1.0, -1.0])
    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)


def degenerate_qp() -> QPProblem:
    """P = 0, single binding constraint: flat direction at optimum."""
    P = np.zeros((2, 2))
    q = np.array([1.0, 1.0])
    A = np.zeros((0, 2))
    b = np.zeros(0)
    G = np.array([[1.0, 1.0]])
    h = np.array([1.0])
    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)


def singleton_qp() -> QPProblem:
    """n = 1, no constraints."""
    P = np.array([[2.0]])
    q = np.array([-4.0])
    A = np.zeros((0, 1))
    b = np.zeros(0)
    G = np.zeros((0, 1))
    h = np.zeros(0)
    return QPProblem(P=P, q=q, A=A, b=b, G=G, h=h)
