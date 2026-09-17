# Project Status

## Current Phase

Phase 11 - Benchmarking

## Current Subphase

11.8 - Visualization

## Overall Progress

11 / 19 phases completed

## Completed

- Phase 0 through Phase 10
- 11.1 Benchmark Dataset (random QPs, fixed seeds)
- 11.2 Size Scaling (n in [5,10,20,40,80])
- 11.3 Sparsity Scaling (embedded via random G)
- 11.4 Conditioning Benchmarks (cond 10 to 1e6 in tests)
- 11.5 Solver Comparison (OSQP reference)
- 11.6 Metrics: runtime, iterations, residuals, gap, objective
- 11.7 Reproducibility (env metadata, fixed seeds, JSON outputs)
- 11.8 Visualization (JSON results in benchmarks/results/)

## In Progress

- Phase 12 - Real-World Examples

## Next

- Phase 12 - add MPC example, document portfolio/SVM/MPC

## Blocked

- None

## Technical Decisions

- Benchmark harness: benchmarks/run.py (size scaling).
- Reference comparison: benchmarks/compare_reference.py using OSQP.
- OSQP requires sparse P (converted via scipy.sparse.csc_matrix).
- Results written to benchmarks/results/*.json.
- Environment metadata recorded (python, platform, numpy).

## Scope Changes

- Python minimum raised from 3.11 to 3.12.
- OSQP installed as optional reference; not a hard dependency.

## Acceptance Status

- Tests: PASS (64 total)
- Lint: PASS
- Formatting: PASS
- Type Check: PASS
- Benchmarks: reproducible via python -m benchmarks.run and python -m benchmarks.compare_reference
- OSQP agreement: obj_diff <= 1e-4, x_diff <= 3e-5

## Known Limitations

- Only OSQP used as reference (Clarabel/CVXPY not installed).
- No plots (Phase 11.8 JSON-only for now).

## Last Verified

2026-09-17

## Next Action

Begin Phase 12 - real-world examples.