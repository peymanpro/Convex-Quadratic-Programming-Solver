# Primal-Dual Interior-Point Method

## Problem

Standard convex QP:

$$
\min_x \frac{1}{2} x^T P x + q^T x
\quad \text{s.t.} \quad A x = b, \; G x \le h.
$$

## Slack Form

Introduce slack $s \ge 0$ to turn inequalities into equalities:

$$
G x + s = h, \qquad s \ge 0.
$$

## Central Path

For a barrier parameter $\mu > 0$, the perturbed KKT system is

$$
\begin{aligned}
P x + q + A^T y + G^T z &= 0, \\
A x - b &= 0, \\
G x + s - h &= 0, \\
s_i z_i &= \mu, \quad i = 1, \dots, p, \\
s > 0, \; z &> 0.
\end{aligned}
$$

As $\mu \to 0$, the solution $(x(\mu), y(\mu), z(\mu), s(\mu))$ approaches
the optimal solution of the original QP.

## Newton Step

Linearizing the perturbed KKT system around the current iterate
gives a linear system in $(dx, dy, dz, ds)$:

$$
\begin{bmatrix}
P    & 0 & A^T & G^T \\
0    & Z & 0   & S   \\
A    & 0 & 0   & 0   \\
G    & I & 0   & 0
\end{bmatrix}
\begin{bmatrix} dx \\ ds \\ dy \\ dz \end{bmatrix}
=
\begin{bmatrix} -r_d \\ -r_c \\ -r_p \\ -r_g \end{bmatrix}
$$

where $Z = \mathrm{diag}(z)$, $S = \mathrm{diag}(s)$, and

$$
r_d = P x + q + A^T y + G^T z, \quad
r_p = A x - b, \quad
r_g = G x + s - h, \quad
r_c = s \odot z - \mu \mathbf{1}.
$$

Eliminating $ds, dz$ reduces this to the symmetric reduced KKT system

$$
\begin{bmatrix} P + G^T W G & A^T \\ A & 0 \end{bmatrix}
\begin{bmatrix} dx \\ dy \end{bmatrix}
=
\begin{bmatrix} b_x \\ b_y \end{bmatrix},
\qquad W = \mathrm{diag}(z_i / s_i),
$$

with

$$
b_x = -r_d + G^T (r_c / s) - G^T W r_g, \qquad b_y = -r_p.
$$

Then

$$
ds = -r_g - G \, dx, \qquad dz = (-r_c - z \odot ds) / s.
$$

## Step Length

To keep $s > 0$ and $z > 0$, use a fraction-to-boundary rule with
parameter $\eta \in (0, 1)$, for example $\eta = 0.995$:

$$
\alpha_p = \min\!\left(1, \; \eta \min_{ds_i < 0} \frac{-s_i}{ds_i}\right),
\qquad
\alpha_d = \min\!\left(1, \; \eta \min_{dz_i < 0} \frac{-z_i}{dz_i}\right).
$$

Then take $\alpha = \min(\alpha_p, \alpha_d)$.

## Barrier Update

After the step, recompute

$$
\mu = \frac{1}{p} \sum_{i=1}^p s_i z_i.
$$

The basic IPM used here shrinks $\mu$ indirectly through the step;
Mehrotra predictor-corrector (Phase 6) uses an explicit adaptive
centering parameter.

## Stopping Criteria

A solve is declared optimal when all of the following hold:

$$
\|r_p\|_\infty \le \varepsilon, \quad
\|r_g\|_\infty \le \varepsilon, \quad
\|r_d\|_\infty \le \varepsilon, \quad
s^T z \le \varepsilon.
$$

with default $\varepsilon = 10^{-8}$.

## Failure States

- `max_iter`: iteration budget exhausted without meeting tolerances.
- `numerical_failure`: reduced KKT matrix is singular or the linear solve fails.

## Implementation Mapping

| Concept | Module |
| --- | --- |
| Residual computation | `solver/residuals.py` |
| IPM iteration | `solver/ipm.py` |
| Convergence tracking | `solver/diagnostics.py` |
| Tests | `tests/test_ipm.py` |

