"""Domain exceptions for the convex QP solver."""

from __future__ import annotations


class QPError(Exception):
    """Base class for all solver domain errors."""


class InvalidProblem(QPError):
    """Problem data is malformed or missing required fields."""


class NonConvexProblem(QPError):
    """The quadratic term P is not positive semidefinite."""


class DimensionMismatch(QPError):
    """Array dimensions are inconsistent across problem data."""


class NumericalFailure(QPError):
    """A numerical breakdown occurred during solution."""


class InfeasibleProblem(QPError):
    """The feasible set is empty."""


class UnboundedProblem(QPError):
    """The objective is unbounded below on the feasible set."""
