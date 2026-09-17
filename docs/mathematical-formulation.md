# Mathematical Formulation

## Problem

We solve the standard convex quadratic program (QP):

$$
\min_{x \in \mathbb{R}^n} \; \frac{1}{2} x^T P x + q^T x
$$

subject to

$$
A x = b, \qquad G x \le h,
$$

where

- $P \in \mathbb{R}^{n \times n}$ is symmetric positive semidefinite,
- $q \in \mathbb{R}^n$,
- $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$ (equality constraints),
- $G \in \mathbb{R}^{p \times n}$, $h \in \mathbb{R}^p$ (inequality constraints).

## Assumptions

1. $P = P^T$ (symmetry).
2. $P \succeq 0$ (positive semidefinite), so the objective is convex.
3. All data are finite; no `NaN` or `Inf` entries.
4. The feasible set is nonempty unless the problem is reported infeasible.
5. The problem is bounded below unless reported unbounded.

## Convexity

A function $f : \mathbb{R}^n \to \mathbb{R}$ is convex if for all $x, y$ and $\theta \in [0,1]$,

$$
f(\theta x + (1 - \theta) y) \le \theta f(x) + (1 - \theta) f(y).
$$

For a twice-differentiable $f$, convexity is equivalent to

$$
\nabla^2 f(x) \succeq 0 \quad \text{for all } x.
$$

For the QP objective $f(x) = \tfrac{1}{2} x^T P x + q^T x$ we have

$$
\nabla f(x) = P x + q, \qquad \nabla^2 f(x) = P.
$$

Therefore the QP is convex if and only if $P \succeq 0$. Equality and inequality constraints are affine, hence the feasible set is convex.

## Positive Semidefinite Matrices

A symmetric matrix $P \in \mathbb{R}^{n \times n}$ is positive semidefinite, written $P \succeq 0$, if

$$
z^T P z \ge 0 \quad \text{for all } z \in \mathbb{R}^n.
$$

Equivalently, every eigenvalue of $P$ is nonnegative:

$$
\lambda_{\min}(P) \ge 0.
$$

In the implementation, convexity is verified by (a) checking symmetry within a tolerance and (b) checking the smallest eigenvalue (or its symmetric part's eigenvalue) is $\ge -\varepsilon_{\text{psd}}$.

## Lagrangian

Introduce Lagrange multipliers $\nu \in \mathbb{R}^m$ for the equalities and $\lambda \in \mathbb{R}_{\ge 0}^p$ for the inequalities. The Lagrangian is

$$
\mathcal{L}(x, \nu, \lambda)
= \frac{1}{2} x^T P x + q^T x
+ \nu^T (A x - b)
+ \lambda^T (G x - h).
$$

See `kkt-conditions.md` for the first-order optimality system.

## Non-Goals

This solver targets convex QP only. The following are explicitly out of scope:

- non-convex QP (i.e. $P \not\succeq 0$),
- mixed-integer QP,
- semidefinite programming (SDP),
- second-order cone programming (SOCP).

## Implementation Mapping

| Concept | Module |
| --- | --- |
| Problem data $P, q, A, b, G, h$ | `solver/problem.py` |
| Convexity check on $P$ | `solver/validation.py` |
| KKT system | `solver/kkt.py` |
| Analytical examples | `validation/analytical_examples.py` |