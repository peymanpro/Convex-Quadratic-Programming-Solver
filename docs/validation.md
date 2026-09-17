# Validation

## Layers of Evidence

1. **Analytical problems** — closed-form solutions in `validation/analytical_examples.py`.
2. **Random feasible QPs** — 50 problems with known strictly feasible interior point.
3. **Mixed problems** — 20 QPs with both equalities and inequalities.
4. **Ill-conditioned problems** — condition numbers up to 1e6.
5. **Failure modes** — contradictory inequalities return non-optimal status.
6. **Edge cases** — singleton, P = 0, box, scaled P.
7. **KKT property tests** — Hypothesis-generated QPs verified against KKT residual bounds.
8. **Reference comparison** — objective and solution agreement with OSQP.

## Tolerances

For optimal solutions:

$$
\|r_p\|_\infty \le 10^{-6}, \quad \|r_d\|_\infty \le 10^{-6},
\quad s^T z \le 10^{-6}.
$$

## Reference Agreement (OSQP)

For random QPs of size n = 5, 10, 20, 40:

- objective difference `<= 1e-4`
- solution difference `<= 3e-5`

Results are recorded in `benchmarks/results/reference_compare.json`.

