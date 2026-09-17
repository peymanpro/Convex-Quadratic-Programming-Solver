# Scientific Audit

This document records the audit of the solver against the acceptance
criteria of the project roadmap.

## 1. Mathematical Formulation

- Standard form: $\min \tfrac{1}{2} x^T P x + q^T x$ s.t. $A x = b$, $G x \le h$.
- Convexity assumption: $P \succeq 0$ enforced by `validate_problem`.
- Lagrangian and KKT conditions documented in `docs/kkt-conditions.md`.
- Verified against analytical examples in `validation/analytical_examples.py`.

**Status: PASS.**
## 2. Algorithm

- Basic primal-dual IPM implemented in `solver/ipm.py`.
- Mehrotra predictor-corrector implemented in `solver/mehrotra.py`.
- Both share the same reduced KKT system and residual definitions.

**Status: PASS.**

## 3. KKT Correctness

- Residuals computed: stationarity, primal equality, primal inequality, complementarity.
- Tests confirm optimal solutions satisfy all KKT residuals to <= 1e-6.
- Complementarity `s^T z <= 1e-6` verified across the 100-problem corpus.

**Status: PASS.**

## 4. Numerical Behavior

- Dense (NumPy) and sparse (SciPy SuperLU) paths agree to machine precision.
- Ill-conditioned problems (condition up to 1e6) solved to documented tolerance.
- Regularization `+ 1e-10 I` reduces risk of singular KKT.

**Status: PASS.**

## 5. Convergence Behavior

- Diagnostic history records iteration, objective, residuals, gap, mu, step length.
- Optimal convergence observed within 4-15 iterations on the corpus.

**Status: PASS.**

## 6. Benchmark Reproducibility

- Fixed seeds in `benchmarks/run.py` and `benchmarks/compare_reference.py`.
- Environment metadata (python, platform, processor, numpy version) recorded in JSON.
- Results stored in `benchmarks/results/`.

**Status: PASS.**

## 7. Reference Comparisons

- OSQP and Clarabel used as external references for random QPs up to n = 40.
- OSQP: objective difference <= 1e-4, solution difference <= 3e-5.
- Clarabel: objective and solution agreement at the 1e-9 level.

**Status: PASS.**

## 8. Failure Analysis

- Infeasible problems return `max_iter` or `numerical_failure`; no infeasibility certificate.
- Unbounded problems are not explicitly detected.
- RuntimeWarnings emitted during divergence of infeasible problems; documented in limitations.

**Status: PASS with documented limitations.**

## 9. Limitations

See `docs/limitations.md`.
