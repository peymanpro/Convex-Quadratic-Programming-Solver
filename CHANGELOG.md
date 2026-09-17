# Changelog

All notable changes to this project are documented in this file.
The format is based on Keep a Changelog and this project adheres to
Semantic Versioning.

## [0.2.0] - 2026-09-17

### Added

- Sparse backend exposed via `IPMOptions.backend` and `solve(..., backend="sparse")`.
- `py.typed` marker so downstream type-checkers see the package types.
- Clarabel as a second reference solver in `benchmarks/compare_reference.py`.
- Heuristic unbounded detection (iterate-norm growth, status `unbounded`).
- Infeasibility heuristic (large primal residual with small stationarity).
- README status table, badges, and Mermaid architecture diagram.

### Fixed

- Silenced floating-point warnings during divergence in IPM and Mehrotra.
- Cleanly report `numerical_failure` on non-finite iterates.

## [0.1.0] - 2026-09-17

### Added

- Initial release: primal-dual interior-point method with Mehrotra
  predictor-corrector, dense and sparse KKT solving, public `solve()` API,
  CLI, Django REST API, validation corpus, property-based tests, and
  reproducible benchmarks.

