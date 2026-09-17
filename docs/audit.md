# Scientific Audit

This document audits the solver against the project roadmap. Each section
is classified as one of: PASS, PARTIAL, NOT IMPLEMENTED, or LIMITATION.
Every PASS claim is supported by code, tests, or benchmark evidence.

Audit date: 2026-09-17.
Canonical release audited: v0.2.0.

## 1. Mathematical Formulation - PASS

- Standard QP: $\min \frac{1}{2} x^T P x + q^T x$ s.t. $A x = b$, $G x \le h$.
- Convexity ($P \succeq 0$) enforced by `solver/validation.py::validate_problem`.
- KKT system derived and documented in `docs/kkt-conditions.md`.
- Verified against closed-form problems in `validation/analytical_examples.py` (3/3 pass).

## 2. Algorithm - PASS

- Basic primal-dual IPM implemented in `solver/ipm.py`.
- Mehrotra predictor-corrector implemented in `solver/mehrotra.py` with the
  classic centering parameter $\sigma = \min(1, (\mu_{\mathrm{aff}} / \mu)^3)$ and
  a second-order corrector term.
- Both share the same reduced KKT system, residual definitions, and
  fraction-to-boundary step rule.

## 3. KKT Correctness - PASS

- Residuals computed in `solver/residuals.py`: stationarity, primal equality,
  primal inequality, complementarity.
- Optimal solutions satisfy all residuals to at most 1e-6 across the corpus
  in `tests/test_corpus.py` and `tests/test_properties.py`.
- Complementarity $s^T z \le 10^{-6}$ verified in `tests/test_ipm.py`.

## 4. Numerical Behavior - PASS

- Dense and sparse backends agree to machine precision on the same problem
  (see `tests/test_sparse_backend.py` and `benchmarks/results/size_scaling.json`).
- Sparse path is native: the reduced KKT is assembled as a CSC matrix in
  `solver/linear_solver.py::assemble_kkt` without constructing a dense
  intermediate.
- Ill-conditioned problems (condition up to 1e6) solved in `tests/test_sparse.py`.
- Regularization `+ 1e-10 I` on the (1,1) block reduces risk of singular KKT.

## 5. Convergence Behavior - PASS

- Diagnostic history records iteration, objective, primal/dual residuals,
  duality gap, barrier parameter mu, and step length (`solver/ipm.py`).
- Optimal convergence observed within 4-20 iterations across the corpus.

## 6. Benchmark Reproducibility - PASS

- Fixed seeds in `benchmarks/run.py` and `benchmarks/compare_reference.py`.
- Environment metadata (python, platform, processor, numpy version) recorded
  in every JSON result.
- All JSON results committed under `benchmarks/results/`.

## 7. Reference Comparisons - PASS

- OSQP and Clarabel used as external references on random QPs up to n = 40.
- OSQP: objective difference at most 1e-4, solution difference at most 3e-5.
- Clarabel: objective and solution agreement at the 1e-9 level.
- Both reference solvers are required (fail-fast) in
  `benchmarks/compare_reference.py`; they are declared under the optional
  `bench` dependency group.

## 8. Failure Analysis - LIMITATION

- Infeasible problems: heuristic detection in `solver/ipm.py` and
  `solver/mehrotra.py`. Detection is not guaranteed for every infeasible
  problem; `tests/test_infeasible.py` asserts one reliable case and
  documents the limits of the heuristic in others. No formal infeasibility
  certificate is produced.
- Unbounded problems: heuristic detection based on iterate-norm growth
  (> 1e10). `tests/test_unbounded.py` asserts one reliable case and
  documents cases where the heuristic does not fire.
- These limitations are recorded in `docs/limitations.md`.

## 9. Docker - PASS

- The Dockerfile is present and internally consistent.
- Docker verification is provided by GitHub Actions CI: the image was
  successfully built and the container health and version endpoints were
  verified in the `docker` CI job.
- Local development-environment Docker execution is not the evidence used
  for this PASS claim.

## 10. CI - PASS

- `.github/workflows/ci.yml` has three jobs:
  (a) quality: ruff check, ruff format --check, mypy, pytest with coverage on Python 3.12 and 3.13;
  (b) docker: builds the Dockerfile and verifies /api/v1/health/ and /api/v1/version/ respond;
  (c) reference-benchmark: installs the optional bench group and runs `python -m benchmarks.compare_reference`.
- `.github/workflows/release.yml` builds sdist and wheel on `v*` tags.

## 11. Coverage - PASS

- Configured under `[tool.coverage]` in `pyproject.toml`.
- Measured source: `solver` package only.
- Threshold: 90 percent. Current: ~93 percent (see CI output).

## 12. Release and Version Consistency - PASS

- Canonical released version: v0.2.0 (`pyproject.toml`, `solver/__init__.py`).
- Current release: v0.2.0. Previous release: v0.1.0.
- CHANGELOG and release notes match.

## Summary

| Category | Status |
| --- | --- |
| Formulation | PASS |
| Algorithm | PASS |
| KKT correctness | PASS |
| Numerical behavior | PASS |
| Convergence | PASS |
| Benchmarks | PASS |
| Reference comparison | PASS |
| Failure analysis | LIMITATION (documented) |
| Docker | PASS |
| CI | PASS |
| Coverage | PASS |
| Version consistency | PASS |

