# Project Status

## Current Phase

Post-Release Corrective Audit

## Current Subphase

Final Consistency & Cleanup

## Overall Progress

- Original roadmap: 19 / 19 phases complete.
- Corrective audit: complete.
- Final consistency cleanup: complete.

## Completed

- Phases 0 through 19 (original roadmap).
- Release v0.1.0 (tag, pushed).
- Release v0.2.0 (tag, pushed).
- Corrective audit issues 1-15 addressed.
- Final consistency & cleanup audit complete.

## In Progress

- None

## Next

- Maintenance only. Possible future extensions: presolve, warm-start,
  additional reference solvers, notebook examples.
- Optional: cut v0.2.1 patch tag if further fixes are shipped.

## Blocked

- None

## Technical Decisions

- Current release: v0.2.0. Previous release: v0.1.0.
- Reference solvers (OSQP, Clarabel) declared under optional bench group.
- Sparse backend is native (CSC assembly via scipy.sparse.bmat in
  solver/linear_solver.py::assemble_kkt).
- Dense and sparse produce identical optima to machine precision.
- Infeasibility and unboundedness are heuristic; documented as limitations.
- Coverage scope: source = solver only.
- Only one canonical sparse KKT assembly path (assemble_kkt);
  build_reduced_kkt_sparse has been removed.

## Scope Changes

- Python minimum 3.12 (from numpy 2.x stub requirements).

## Acceptance Status

- Tests: 84 collected, 84 passing.
- Lint: PASS.
- Formatting: PASS.
- Type Check: PASS.
- Coverage (source = solver): 93 percent (threshold 90 percent).
- Analytical KKT checks: 3/3 pass.
- Dense-vs-sparse benchmark: PASS.
- Reference comparison (OSQP + Clarabel): PASS.
- Docker: PASS (verified by GitHub Actions CI build and container health).
- Documentation: PASS.

## Known Limitations

- Infeasibility and unboundedness detection are heuristic; not every
  infeasible or unbounded problem is guaranteed to be flagged.
- Dense backend is faster than sparse for the benchmark family tested
  (n up to 160). No sparse speedup claim is made at those sizes.
- See docs/limitations.md.

## Last Verified

2026-09-17

## Next Action

None. Repository is in final consistent state.