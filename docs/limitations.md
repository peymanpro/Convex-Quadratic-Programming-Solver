# Limitations

- Convex QP only. Non-convex QP is rejected during validation.
- No integer variables, no SDP, no SOCP.
- Infeasible problems are reported as `max_iter` or `numerical_failure`; no
  dedicated infeasibility certificate is produced.
- Unbounded problems are not explicitly detected.
- All problems must have finite data (NaN/Inf rejected).
- Dense path is O(n^3) memory; sparse path relies on SciPy SuperLU.
- Reference comparison uses OSQP only (Clarabel/CVXPY not installed here).
- Docker build has not been executed locally; Dockerfile is provided as-is.

