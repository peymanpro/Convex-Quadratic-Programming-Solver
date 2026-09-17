# Mehrotra Predictor-Corrector

## Idea

Mehrotra's method takes an affine scaling step first to estimate the
achievable reduction in the barrier parameter mu, then chooses the
centering parameter from that estimate, and finally adds a second-order
correction term.

## Steps

1. Affine predictor. Solve the Newton system with the pure
   complementarity residual $r_c^{\mathrm{aff}} = s \odot z$.
   Get $(dx^{\mathrm{aff}}, ds^{\mathrm{aff}}, dz^{\mathrm{aff}})$.

2. Affine step length. Compute $\alpha_p^{\mathrm{aff}}$ and
   $\alpha_d^{\mathrm{aff}}$ by fraction-to-boundary, then

$$
\mu_{\mathrm{aff}} = \frac{(s + \alpha_p^{\mathrm{aff}} ds^{\mathrm{aff}})^T (z + \alpha_d^{\mathrm{aff}} dz^{\mathrm{aff}})}{p}.
$$

3. Centering parameter.

$$
\sigma = \min\left(1, \left(\frac{\mu_{\mathrm{aff}}}{\mu}\right)^3\right).
$$

4. Corrector. Solve again with

$$
r_c^{\mathrm{cor}} = s \odot z + ds^{\mathrm{aff}} \odot dz^{\mathrm{aff}} - \sigma \mu \mathbf{1}.
$$

5. Combined direction. Take a fraction-to-boundary step in
   $(dx, dy, ds, dz)$ and update $(x, y, s, z)$.

## Implementation Mapping

| Concept | Module |
| --- | --- |
| Predictor / corrector loop | `solver/mehrotra.py` |
| Step length | `solver/ipm.py::_step_length` |
| Residuals | `solver/residuals.py` |

