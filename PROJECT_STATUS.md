# Project Status

## Current Phase

Phase 4 - Inequality Constraints & Slack Variables

## Current Subphase

4.6 - Numerical Tests

## Overall Progress

4 / 19 phases completed

## Completed

- Phase 0 - Project Definition & Development Foundation
- Phase 1 - Mathematical Foundations
- Phase 2 - Problem Model & Validation
- Phase 3 - Equality-Constrained QP
- 4.1 Slack Variables
- 4.2 Primal/Dual Variables
- 4.3 Central Path
- 4.4 Barrier Parameter
- 4.5 Perturbed KKT System
- 4.6 Numerical Tests (10 constrained QPs)

## In Progress

- Phase 5 - Primal-Dual Interior-Point Method (basic IPM already implemented; refinements next)

## Next

- Phase 5 - diagnostics, stopping criteria, failure states
- Phase 6 - Mehrotra predictor-corrector

## Blocked

- None

## Technical Decisions

- Slack form: G x + s = h, s > 0, with dual z > 0.
- Reduced KKT via W = diag(z)/diag(s).
- Newton RHS: bx = -r_d + G^T (r_c / s) - G^T (W r_g), with r_c = s*z - sigma*mu.
- dz = (-r_c - z*ds)/s (sign corrected during debugging).
- Fraction-to-boundary with eta = 0.995.
- Equality-only path uses a single dense KKT solve.
- Regularization: +1e-10 * I on H block.

## Scope Changes

- Python minimum raised from 3.11 to 3.12 to match numpy 2.x stub requirements.

## Acceptance Status

- Tests: PASS (10 IPM tests + prior)
- Lint: PASS
- Formatting: PASS
- Type Check: PASS
- Coverage (solver): ~90 percent
- Constrained QPs solved: 10/10 with status optimal
- Complementarity <= 1e-6 verified
- Duality gap <= 1e-6 verified
- Benchmarks: Not yet implemented

## Known Limitations

- Basic IPM only (Mehrotra predictor-corrector arrives in Phase 6).
- Dense KKT only (sparse in Phase 7).

## Last Verified

2026-09-17

## Next Action

Begin Phase 5 - refine diagnostics, stopping criteria, failure states.