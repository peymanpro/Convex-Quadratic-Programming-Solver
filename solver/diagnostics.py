"""Convergence diagnostics for the IPM solver."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class IterationRecord:
    """One IPM iteration snapshot."""

    iteration: int
    objective: float
    primal_residual: float
    dual_residual: float
    duality_gap: float
    mu: float
    step_length: float = 0.0


@dataclass
class Diagnostics:
    """Trajectory of the IPM solve."""

    records: list[IterationRecord] = field(default_factory=list)

    def add(self, rec: IterationRecord) -> None:
        self.records.append(rec)

    @property
    def iterations(self) -> int:
        return len(self.records)

    def as_dicts(self) -> list[dict[str, float]]:
        return [
            {
                "iteration": float(r.iteration),
                "objective": r.objective,
                "primal_residual": r.primal_residual,
                "dual_residual": r.dual_residual,
                "duality_gap": r.duality_gap,
                "mu": r.mu,
                "step_length": r.step_length,
            }
            for r in self.records
        ]
