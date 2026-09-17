# Release Notes - v0.2.0

Second release. Adds sparse-backend access through the public API,
heuristic infeasibility and unboundedness detection, a second reference
solver (Clarabel), and a polished README with badges and architecture diagram.

## Highlights

- `solve(problem, backend="sparse")` selects SciPy SuperLU automatically.
- `solver/py.typed` published for downstream type-checking.
- Clarabel reference comparison reaches 1e-9 agreement on objective and x.
- Heuristic statuses `unbounded` and `infeasible` for non-optimal cases.
- No floating-point warnings leak to users during divergence.

## Verification

- Tests: 79 passed.
- Lint / format / mypy: clean.
- Coverage (solver): 96 percent.

