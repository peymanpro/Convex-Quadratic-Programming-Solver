# Release Notes - v0.1.0

Initial release of the Convex Quadratic Programming Solver.

## Highlights

- Primal-dual interior-point method with Mehrotra predictor-corrector.
- Dense and sparse KKT solving (NumPy / SciPy SuperLU).
- Public solver.solve(problem) API with stable SolverResult.
- CLI: cqp-solve problem.json.
- Django REST API with OpenAPI / Swagger UI.
- 100+ problem numerical validation corpus.
- Hypothesis property-based tests.
- Reference comparison against OSQP.
- Reproducible benchmarks with recorded environment metadata.

## Verification

- Tests: 73 passed (unit, integration, property-based, API).
- Lint: ruff check . clean.
- Format: ruff format --check . clean.
- Type check: mypy . clean.
- Coverage: 96 percent on solver package.
- Analytical KKT checks: 3/3 pass.
- Reference agreement with OSQP: objective diff <= 1e-4.

## Known Limitations

See docs/limitations.md.

