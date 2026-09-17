# Benchmarks

Reproducible benchmarks. Every result row records the environment metadata.

## Size Scaling and Dense vs Sparse

Command:

```powershell
python -m benchmarks.run
```

Sizes: n in {10, 20, 40, 80, 160} with p = n // 2. Fixed seed = 0.
Both dense and sparse backends are recorded for each problem and each
method (mehrotra, ipm).

Metrics recorded per row: n, p, backend, method, status, iterations,
runtime, primal residual, dual residual, duality gap, objective.

Output: benchmarks/results/size_scaling.json.

### Observed behavior (Windows 10, Python 3.12, numpy 2.5.3)

For this benchmark family the KKT systems are small (n + m up to 160) and
the reduced KKT matrix stays moderately dense because of G^T W G. On this
hardware the dense path is faster than the sparse path for all tested
sizes; sparse timings grow faster here because SuperLU setup overhead
dominates at small scale.

Sparse mode is genuinely sparse-native (no dense intermediate) and
numerically matches dense (see tests/test_sparse_backend.py). It is
expected to become beneficial when the KKT sparsity pattern is exploited
at larger n or with structured G (e.g., banded constraints), which we
have not benchmarked yet.

We report this outcome honestly: no speedup claim is made for sparse
mode at these sizes.

## Reference Comparison

Command:

```powershell
python -m benchmarks.compare_reference
```

Compares against OSQP and Clarabel on random QPs.

Output: benchmarks/results/reference_compare.json.

Requires the optional benchmark environment (see below).

## Benchmark Environment

Reference solvers are optional. Install them with:

```powershell
pip install -e ".[bench]"
```

The benchmark scripts fail clearly if a requested reference solver is
missing, instead of silently skipping.

## Reproducibility

Every benchmark records python version, platform, processor, and numpy
version. Fixed seeds are used. All JSON results are stored in the
repository.

