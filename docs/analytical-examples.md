# Analytical Examples

Three closed-form convex QP examples used to validate KKT residuals.
Each example corresponds to a function in `validation/analytical_examples.py`
and is checked against the KKT system in `docs/kkt-conditions.md`.

## Example 1 - Unconstrained QP in 2D

**Problem**

$$
\min_{x \in \mathbb{R}^2} \; \frac{1}{2} x^T P x + q^T x, \quad P = I_2, \quad q = \begin{bmatrix} -1 \\ -2 \end{bmatrix}.
$$

Stationarity $P x^\star + q = 0$ gives $x^\star = [1, 2]^T$. KKT residual is zero to machine precision.
---

## Example 2 - Equality-Constrained QP in 2D

**Problem**

$$
\min_{x \in \mathbb{R}^2} \; \frac{1}{2} x^T P x + q^T x
\quad \text{s.t.} \quad A x = b,
$$

with

$$
P = I_2, \quad q = 0, \quad A = \begin{bmatrix} 1 & 1 \end{bmatrix}, \quad b = 1.
$$

**KKT system**

$$
\begin{bmatrix} I_2 & A^T \\ A & 0 \end{bmatrix}
\begin{bmatrix} x \\ \nu \end{bmatrix}
=
\begin{bmatrix} -q \\ b \end{bmatrix}.
$$

Stationarity gives $x = -\nu [1, 1]^T$. With $x_1 + x_2 = 1$ we get $\nu^\star = -\tfrac{1}{2}$ and $x^\star = [1/2, 1/2]^T$.

---

## Example 3 - Inequality-Constrained QP in 2D

**Problem**

$$
\min_{x \in \mathbb{R}^2} \; \frac{1}{2}(x_1 - 2)^2 + \frac{1}{2}(x_2 - 3)^2
\quad \text{s.t.} \quad x_1 + x_2 \le 2.
$$

**QP form**

$$
P = I_2, \quad q = \begin{bmatrix} -2 \\ -3 \end{bmatrix}, \quad
G = \begin{bmatrix} 1 & 1 \end{bmatrix}, \quad h = 2.
$$

The constraint is active: $x_1 + x_2 = 2$. From stationarity,

$$
x = \begin{bmatrix} 2 - \lambda \\ 3 - \lambda \end{bmatrix},
\quad (2 - \lambda) + (3 - \lambda) = 2
\;\Rightarrow\; \lambda^\star = \tfrac{3}{2}.
$$

So $x^\star = [1/2, 3/2]^T$ and $\lambda^\star = 3/2$.

---

## Verification Command

```powershell
python validation\analytical_examples.py
```

Expected output: three PASS lines, each with worst KKT residual `0.00e+00`.

