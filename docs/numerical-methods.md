# Numerical Methods

## Reduced KKT System

Each interior-point iteration solves a symmetric reduced KKT system:

$$
\begin{bmatrix} H & A^T \\ A & 0 \end{bmatrix}
\begin{bmatrix} dx \\ dy \end{bmatrix}
= \begin{bmatrix} b_x \\ b_y \end{bmatrix},
\qquad H = P + G^T W G, \; W = \mathrm{diag}(z_i / s_i).
$$

The slack and dual directions follow by elimination:

$$
ds = -r_g - G\,dx, \qquad dz = (-r_c - z \odot ds) / s.
$$

## Dense vs Sparse

- Dense: `numpy.linalg.solve` (LAPACK).
- Sparse: `scipy.sparse.linalg.splu` (SuperLU) on a CSC matrix.
- Selection via `LinearSolverOptions(backend, sparse_threshold)`.

## Regularization

A small diagonal shift `+ eps I` with `eps = 1e-10` is added to `H`
to reduce the risk of singular KKT matrices near the boundary.

## Step Length

Fraction-to-boundary with `eta = 0.995`:

$$
\alpha_p = \min\!\left(1, \eta \min_{ds_i < 0} \frac{-s_i}{ds_i}\right),
\quad
\alpha_d = \min\!\left(1, \eta \min_{dz_i < 0} \frac{-z_i}{dz_i}\right).
$$

## Conditioning

Pseudo-condition numbers up to $10^6$ are covered in tests.
Ill-conditioned problems use the same regularization and step rules.

