"""Model Predictive Control (MPC) example.

Linear double integrator:
    x_{k+1} = A x_k + B u_k
with state x = [position, velocity] and control u (acceleration).

MPC: minimize sum over horizon of (x_k - x_ref)^T Q (x_k - x_ref) + u_k^T R u_k
subject to |u_k| <= u_max.

This is a QP in the stacked control vector U = [u_0, ..., u_{N-1}].
"""

from __future__ import annotations

import numpy as np

from solver import QPProblem, solve


def build_mpc_qp(
    N: int = 10,
    dt: float = 0.1,
    x0: np.ndarray | None = None,
    x_ref: np.ndarray | None = None,
    u_max: float = 1.0,
) -> QPProblem:
    if x0 is None:
        x0 = np.array([0.0, 0.0])
    if x_ref is None:
        x_ref = np.array([1.0, 0.0])

    A = np.array([[1.0, dt], [0.0, 1.0]])
    B = np.array([[0.5 * dt * dt], [dt]])
    Q = np.diag([10.0, 1.0])
    R = np.array([[0.1]])

    # Build prediction matrices: X = Phi x0 + Gamma U
    n = 2
    Phi = np.zeros((N * n, n))
    Gamma = np.zeros((N * n, N))
    Apow = np.eye(n)
    for i in range(N):
        Apow = A @ Apow
        Phi[i * n : (i + 1) * n, :] = Apow
        for j in range(i + 1):
            Aij = np.linalg.matrix_power(A, i - j) @ B
            Gamma[i * n : (i + 1) * n, j : j + 1] = Aij

    Qbar = np.kron(np.eye(N), Q)
    Rbar = np.kron(np.eye(N), R)

    # Cost: 0.5 U^T P U + q^T U + const
    P = 2.0 * (Gamma.T @ Qbar @ Gamma + Rbar)
    x_ref_stack = np.tile(x_ref, N)
    q = 2.0 * Gamma.T @ Qbar @ (Phi @ x0 - x_ref_stack)

    # Constraints: |u_k| <= u_max
    G = np.vstack([np.eye(N), -np.eye(N)])
    h = np.concatenate([u_max * np.ones(N), u_max * np.ones(N)])

    return QPProblem(
        P=P,
        q=q,
        A=np.zeros((0, N)),
        b=np.zeros(0),
        G=G,
        h=h,
    )


def main() -> None:
    problem = build_mpc_qp()
    result = solve(problem)
    print("status =", result.status)
    print("iterations =", result.iterations)
    print("control sequence =", np.round(result.x, 4))
    print("objective =", result.objective)


if __name__ == "__main__":
    main()
