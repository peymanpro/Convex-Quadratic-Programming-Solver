# Project Status

## Current Phase

Post-Release Corrective Audit

## Current Subphase

Phase 19 (original) conceptually complete; corrective audit in progress.

## Overall Progress

19 / 19 original roadmap phases conceptually complete.
Corrective audit: in progress.

## Completed

- Phases 0 through 18 (original roadmap).
- Phase 19.1 - 19.5 (README, benchmark report, architecture, example gallery, release notes).
- Release v0.1.0 (tag, pushed).
- Release v0.2.0 (tag, pushed): sparse backend API, py.typed, Clarabel reference, unbounded/infeasible heuristics, README polish.

## In Progress

- Post-Release Corrective Audit (issues 1-14 from external review).

## Next

- Sparse-native KKT assembly path (Issue 3).
- Dense-vs-sparse benchmark (Issue 4).
- Benchmark dependency group (Issue 5).
- Tighten infeasible / unbounded tests (Issues 6, 7).
- Documentation corrections (Issues 8, 9).
- Rewrite audit.md (Issue 10).
- Verify Docker (Issue 11) and CI (Issue 12).

## Blocked

- None

## Technical Decisions

- Canonical released version: v0.2.0 (current).
- Historical releases preserved: v0.1.0, v0.2.0.
- Version source of truth: pyproject.toml.
- Coverage measured for source = solver only (not whole repo).

## Scope Changes

- Python minimum 3.12 (from numpy 2.x stub requirements).

## Acceptance Status

- Tests: 79 collected, 79 passing.
- Lint: PASS
- Formatting: PASS
- Type Check: PASS
- Coverage (source = solver): 93.21% (threshold 90%).
- Analytical KKT checks: 3/3 pass.
- References: OSQP and Clarabel comparisons available.

## Known Limitations

- See docs/limitations.md.
- Sparse path currently converts a dense KKT to CSC; sparse-native assembly in progress.

## Last Verified

2026-09-17

## Next Action

Fix version/test/coverage inconsistency across README and PROJECT_STATUS.