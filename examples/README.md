# Real-World Examples

Each example documents the problem, its mathematical formulation,
the reduction to standard convex QP form, the solver invocation, and
interpretation of results.

Run any example with:

```powershell
python examples\<name>.py
```

---

## 1. Portfolio Optimization (`portfolio.py`)

**Problem.** Allocate capital across assets to minimize variance subject
to a budget and non-negativity.

**Formulation.**

$$
\min_w \; w^T S w \quad \text{s.t.} \quad \sum_i w_i = 1, \; w \ge 0.
$$

**QP transformation.** With $P = 2S$, $q = 0$, $A = \mathbf{1}^T$, $b = 1$,
$G = -I$, $h = 0$, the model matches the standard form.

**Result (sample).** $w^\star = [0.727, 0.273]$, objective $= 0.0318$.

**Interpretation.** The lower-risk asset receives the larger weight;
the weight on the second asset is driven by its higher variance.

---

## 2. Resource Allocation (`resource_allocation.py`)

**Problem.** Distribute a limited budget across projects to maximize
concave utility.

**Formulation.**

$$
\max_x \; c^T x - \tfrac{1}{2} x^T x \quad \text{s.t.} \quad \mathbf{1}^T x \le 1, \; x \ge 0.
$$

**QP transformation.** $P = I$, $q = -c$, $G$ stacks the budget and
non-negativity inequalities, $h$ combines budget and zeros.

**Result (sample).** $x^\star \approx [0, 0, 1]$, objective $= -2.5$.

**Interpretation.** The highest-utility project consumes the entire
budget at the optimum, consistent with diminishing returns.

---

## 3. Support Vector Machine (Dual) (`svm_dual.py`)

**Problem.** Soft-margin SVM dual: find multipliers $\\alpha$ that
maximize the margin.

**Formulation.**

$$
\min_\alpha \; \tfrac{1}{2} \alpha^T Q \alpha - \mathbf{1}^T \alpha
\quad \text{s.t.} \quad y^T \alpha = 0, \; 0 \le \alpha \le C.
$$

with $Q_{ij} = y_i y_j (x_i^T x_j)$ (here a small identity-regularized kernel).

**QP transformation.** $P = Q$, $q = -\mathbf{1}$, $A = y^T$, $b = 0$,
$G$ encodes box constraints.

**Result (sample).** $\\alpha^\star = [0.5, 1.0, 0.5]$, objective $= -1.999$.

**Interpretation.** The middle point has the maximum multiplier, so it
acts as a support vector near the decision boundary.

---

## 4. Model Predictive Control (`mpc.py`)

**Problem.** Control a double integrator to a reference state over a
finite horizon, minimizing state and input deviation.

**Formulation.**

$$
\min_{u_0, \dots, u_{N-1}} \; \sum_{k=0}^{N-1}
\left[ (x_k - x_{\text{ref}})^T Q (x_k - x_{\text{ref}}) + u_k^T R u_k \right]
$$

subject to $x_{k+1} = A x_k + B u_k$ and $|u_k| \le u_{\max}$.

**QP transformation.** Stack $U = [u_0, \dots, u_{N-1}]$. With prediction
matrices $X = \Phi x_0 + \Gamma U$, the cost becomes

$$
\tfrac{1}{2} U^T P U + q^T U + \text{const},
$$

where $P = 2(\Gamma^T \bar{Q} \Gamma + \bar{R})$ and
$q = 2 \Gamma^T \bar{Q} (\Phi x_0 - x_{\text{ref,stack}})$.
The constraints are $|u_k| \le u_{\max}$.

**Result (sample).** Control saturates at $u_{\max}$ for the first
seven steps, then decelerates to reach the reference.

**Interpretation.** The active input bound is captured exactly by the
inequality constraints; the terminal behavior is smooth because the
state cost penalizes velocity errors.

---

## Summary Table

| Example | n | Constraints | Active set |
| --- | --- | --- | --- |
| Portfolio | 2 | 1 eq + 2 ineq | both bounds inactive |
| Resource allocation | 3 | 1 ineq + 3 bounds | budget active, one bound active |
| SVM dual | 3 | 1 eq + 6 ineq | active at box edges |
| MPC | 10 | 20 ineq | first 7 inputs at bound |

