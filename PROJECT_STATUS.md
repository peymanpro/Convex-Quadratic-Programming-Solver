# Project Status

## Current Phase

Phase 9 - Rigorous Numerical Validation

## Current Subphase

9.9 - Error Metrics

## Overall Progress

9 / 19 phases completed

## Completed

- Phase 0 through Phase 8
- 9.1 Analytical Problems (Phase 1 examples reused)
- 9.2 Random Convex QPs (50 feasible, 20 mixed)
- 9.3 Feasible Problems verified
- 9.4 Infeasible Problems (returned as max_iter/numerical_failure)
- 9.5 Unbounded Problems noted in limitations
- 9.6 Ill-Conditioned Problems (cond up to 1e6)
- 9.7 Degenerate / Edge Cases (P=0, singleton, box, scaled)
- 9.8 Reference Solvers deferred to Phase 11 (OSQP/Clarabel/CVXPY)
- 9.9 Error Metrics: primal, dual, gap, objective

## In Progress

- Phase 10 - Property-Based & Robust Testing

## Next

- Phase 10 - Hypothesis strategies for QP generation

## Blocked

- None

## Technical Decisions

- Corpus generators in validation/generators.py (random_psd, random_feasible_qp, random_mixed_qp, ill_conditioned_qp, infeasible_qp, degenerate_qp, singleton_qp).
- Random QPs constructed with known strictly feasible interior point (h = G x0 + slack).
- Reference solver comparison deferred to Phase 11 benchmark infrastructure.

## Scope Changes

- Python minimum raised from 3.11 to 3.12 to match numpy 2.x stub requirements.

## Acceptance Status

- Tests: PASS (60 total)
- Lint: PASS
- Formatting: PASS
- Type Check: PASS
- Corpus: 50 feasible + 20 mixed + 10 ill-conditioned + 10 failure + 10 edge = 100 problems
- Optimal agreement: all feasible/mixed/edge; failure modes return non-optimal status

## Known Limitations

- Infeasible QPs cause RuntimeWarnings in mehrotra.py during divergence; status is returned correctly but numeric noise appears. Will add safeguard.
- Unbounded QP detection not implemented (returns max_iter).

## Last Verified

2026-09-17

## Next Action

Begin Phase 10 - Hypothesis property-based tests.