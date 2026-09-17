# Benchmarks

## Size Scaling

Command:

```powershell
python -m benchmarks.run
```

Sizes: n in {5, 10, 20, 40, 80}, p = n // 2. Fixed seed = 0.
Recorded for both `mehrotra` and `ipm`.

Metrics per row: status, iterations, runtime, primal residual, dual residual, duality gap.

Output: `benchmarks/results/size_scaling.json`.

## Reference Comparison

Command:

```powershell
python -m benchmarks.compare_reference
```

Compares our solver with OSQP on random QPs. Reports `obj_diff` and `x_diff`.

Output: `benchmarks/results/reference_compare.json`.

## Reproducibility

Every benchmark records python version, platform, processor, and numpy version.
No results are cherry-picked; all outputs are stored in the repository.

