# Architecture

## Layering

```text
CLI / Django API
       |
solver.solve(problem)          <- public API
       |
solver.ipm / solver.mehrotra   <- algorithms
       |
solver.kkt / solver.linear_solver / solver.residuals   <- numerics
       |
solver.problem / solver.validation / solver.exceptions <- data + contracts
```

## Module Responsibilities

| Module | Responsibility |
| --- | --- |
| solver/problem.py | QPProblem dataclass (P, q, A, b, G, h) |
| solver/validation.py | shape, finiteness, symmetry, PSD checks |
| solver/exceptions.py | domain error hierarchy |
| solver/kkt.py | dense and sparse KKT builders; equality solve |
| solver/residuals.py | stationarity, primal, complementarity residuals |
| solver/linear_solver.py | dense (numpy) vs sparse (SuperLU) dispatch |
| solver/ipm.py | basic primal-dual interior-point method |
| solver/mehrotra.py | Mehrotra predictor-corrector |
| solver/diagnostics.py | iteration records for convergence tracking |
| solver/result.py | public SolverResult dataclass |
| solver/cli.py | cqp-solve entry point |
| validation/* | analytical examples and random generators |
| benchmarks/* | size scaling and reference comparison |
| api/solver_service/* | Django adapter (no optimization logic) |

## Dependency Direction

The optimization core has no Django dependency. The API imports the
public `solver.solve` function only. Removing `api/` leaves the solver
fully functional.

