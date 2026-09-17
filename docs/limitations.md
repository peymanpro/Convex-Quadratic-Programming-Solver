# Limitations

- Convex QP only. Non-convex QP (P not PSD) is rejected during validation.
- No integer variables, no SDP, no SOCP.
- Infeasible problems: status is `infeasible` (heuristic), `max_iter`, or
  `numerical_failure` depending on which condition fires first. No formal
  infeasibility certificate is produced.
- Unbounded problems: heuristically detected via iterate-norm growth (> 1e10)
  and reported as status `unbounded`.
- All problems must have finite data (NaN/Inf rejected).
- Dense linear solve: time ~ O((n+m)^3), memory ~ O((n+m)^2),
  where n+m is the reduced KKT dimension (not the original QP size).
- Sparse path relies on SciPy SuperLU.
- Reference comparison uses OSQP and Clarabel.
- Docker build is not executed locally; Dockerfile is provided as-is.

