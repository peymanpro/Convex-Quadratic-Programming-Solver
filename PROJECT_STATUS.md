# Project Status

## Current Phase

Post-Release Corrective Audit

## Current Subphase

Corrective audit in progress - all issues 1-15 addressed; final verification pending.

## Overall Progress

- Original roadmap: 19 / 19 phases conceptually complete.
- Corrective audit: all identified issues (1-15) resolved.

## Completed

- Phases 0 through 19 (original roadmap).
- Release v0.1.0 (tag, pushed).
- Release v0.2.0 (tag, pushed).
- Corrective Issue 1: version metadata synchronized.
- Corrective Issue 2: test count (84) consistent across README and PROJECT_STATUS.
- Corrective Issue 3: sparse-native KKT assembly (no dense intermediate).
- Corrective Issue 4: dense-vs-sparse benchmark; honest findings documented.
- Corrective Issue 5: optional `bench` dependency group; fail-fast on missing references.
- Corrective Issue 6: strict infeasibility test plus documented heuristic limits.
- Corrective Issue 7: strict unboundedness test plus documented heuristic limits.
- Corrective Issue 8: dense memory complexity corrected (time O((n+m)^3), memory O((n+m)^2)).
- Corrective Issue 9: LaTeX audit; mehrotra-algorithm.md rewritten; all docs balanced.
- Corrective Issue 10: docs/audit.md rewritten with PASS/PARTIAL/LIMITATION classification.
- Corrective Issue 11: Docker verified - image builds, container serves API (health, version).
- Corrective Issue 12: CI includes quality (3.12/3.13), docker build, reference benchmark jobs.
- Corrective Issue 13: coverage measured (source = solver), 93 percent, threshold 90.
- Corrective Issue 14: PROJECT_STATUS reflects corrective stage.
- Corrective Issue 15: no unnecessary technologies introduced.

## In Progress

- Final commit and push of the corrective audit.

## Next

- Push to origin.
- Optional: cut v0.2.1 patch release with corrective fixes.

## Blocked

- None

## Technical Decisions

- Canonical released version: v0.2.0.
- Historical releases preserved: v0.1.0, v0.2.0.
- Reference solvers (OSQP, Clarabel) declared under optional `bench` group.
- Sparse backend is native (CSC assembly via scipy.sparse.bmat).
- Dense and sparse produce identical optima to machine precision.
- Infeasibility and unboundedness are heuristic; documented as LIMITATION.
- Coverage scope: source = solver only.

## Scope Changes

- Python minimum 3.12 (from numpy 2.x stub requirements).

## Acceptance Status

- Tests: 84 collected, 84 passing.
- Lint: PASS.
- Formatting: PASS.
- Type Check: PASS.
- Coverage (source = solver): 93.10% (threshold 90%).
- Analytical KKT checks: 3/3 pass.
- Dense-vs-sparse benchmark: PASS (results in benchmarks/results/size_scaling.json).
- Reference comparison (OSQP + Clarabel): PASS.
- Docker: PASS (build + container health verified).
- Documentation: PASS (audit rewritten, LaTeX clean, complexity corrected).

## Known Limitations

- Infeasibility and unboundedness detection are heuristic; not every
  infeasible or unbounded problem is guaranteed to be flagged.
- Dense backend is faster than sparse for the benchmark family tested
  (n up to 160). No sparse speedup claim is made at those sizes.
- See docs/limitations.md.

## Last Verified

2026-09-17

## Next Action

Commit final corrective audit and push to origin.