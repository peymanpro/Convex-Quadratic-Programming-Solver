# Mehrotra Predictor-Corrector

## Idea

Instead of using a fixed centering parameter, Mehrotra's method takes
an affine scaling step first to estimate the achievable reduction in mu,
then chooses the centering parameter from that estimate, and finally
adds a second-order correction term.

## Steps

1. **Affine predictor** — solve the Newton system with the pure
   complementarity residual $r_c^{aff} = s \odot z$.
   Get $(dx^{aff}, ds^{aff}, dz^{aff})$.

2. **Affine step length** — compute $\\alpha^{aff}_p$, $\\alpha^{aff}_d$ by
   fraction-to-boundary, then

$$
\mu_{aff} = \frac{(s + \alpha_p^{aff} ds^{aff})^T (z + \alpha_d^{aff} dz^{aff})}{p}.
$$

3. **Centering parameter**

$$
\sigma = \min\left(1, \left(\frac{\mu_{aff}}{\mu}\right)^3\right).
$$

4. **Corrector** — solve again with

$$
r_c^{cor} = s \odot z + ds^{aff} \odot dz^{aff} - \sigma \mu \mathbf{1}.
$$

5. **Combined direction** — take a fraction-to-boundary step in
   $(dx, dy, ds, dz)$ and update $(x, y, s, z)$.

## Implementation Mapping

| Concept | Module |
| --- | --- |
| Predictor / corrector loop | `solver/mehrotra.py` |
| Step length | `solver/ipm.py::_step_length` |
| Residuals | `solver/residuals.py` |

