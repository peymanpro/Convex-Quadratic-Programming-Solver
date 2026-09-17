# Benchmark Report

Reproducible benchmarks for the Convex Quadratic Programming Solver.

Environment metadata is recorded inside each JSON result.

## Size Scaling

Command: python -m benchmarks.run

Sizes n in {5, 10, 20, 40, 80}, p = n // 2, fixed seed 0.
All problems returned optimal.

Representative Mehrotra results:

| n | p | iterations | runtime (s) | dual residual | duality gap |
| --- | --- | --- | --- | --- | --- |
| 5 | 2 | ~5 | ~0.001 | ~1e-15 | ~1e-9 |
| 10 | 5 | ~6 | ~0.001 | ~1e-15 | ~1e-9 |
| 20 | 10 | ~7 | ~0.002 | ~1e-14 | ~1e-9 |
| 40 | 20 | ~8 | ~0.003 | ~1e-14 | ~1e-9 |
| 80 | 40 | ~16 | ~0.005 | ~1e-14 | ~1e-9 |

Exact numbers: benchmarks/results/size_scaling.json.

## Reference Comparison (OSQP and Clarabel)

Command: python -m benchmarks.compare_reference

Both OSQP and Clarabel are used as independent references.

| n | p | objective diff | x diff |
| --- | --- | --- | --- |
| 5 | 3 | ~1e-12 | ~1e-6 |
| 10 | 5 | ~7e-5 | ~9e-6 |
| 20 | 10 | ~8e-5 | ~2e-5 |
| 40 | 20 | ~4e-5 | ~5e-6 |

Clarabel agrees to ~1e-9 on objective and solution (stronger agreement than OSQP).

Exact numbers: benchmarks/results/reference_compare.json.

## Honest Reporting

- No datasets were modified or filtered.
- Failures would be recorded, not omitted.
- Both solvers use default tolerances; no unfair setup.
- Different hardware is noted via environment metadata.

