"""Tests for solver.validation."""

from __future__ import annotations

import numpy as np
import pytest

from solver.exceptions import (
    DimensionMismatch,
    InvalidProblem,
    NonConvexProblem,
)
from solver.problem import QPProblem
from solver.validation import validate_problem


def _good() -> QPProblem:
    return QPProblem(
        P=np.eye(2),
        q=np.zeros(2),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.zeros((0, 2)),
        h=np.zeros(0),
    )


def test_valid_problem_passes() -> None:
    validate_problem(_good())


def test_nan_in_q_raises() -> None:
    p = _good()
    bad_q = np.array([np.nan, 0.0])
    p = QPProblem(p.P, bad_q, p.A, p.b, p.G, p.h)
    with pytest.raises(InvalidProblem):
        validate_problem(p)


def test_inf_in_P_raises() -> None:
    p = _good()
    bad_P = np.eye(2)
    bad_P[0, 0] = np.inf
    p = QPProblem(bad_P, p.q, p.A, p.b, p.G, p.h)
    with pytest.raises(InvalidProblem):
        validate_problem(p)


def test_q_wrong_shape_raises() -> None:
    p = _good()
    p = QPProblem(p.P, np.zeros(3), p.A, p.b, p.G, p.h)
    with pytest.raises(DimensionMismatch):
        validate_problem(p)


def test_A_wrong_columns_raises() -> None:
    p = _good()
    p = QPProblem(p.P, p.q, np.zeros((1, 3)), np.zeros(1), p.G, p.h)
    with pytest.raises(DimensionMismatch):
        validate_problem(p)


def test_G_wrong_columns_raises() -> None:
    p = _good()
    p = QPProblem(p.P, p.q, p.A, p.b, np.zeros((2, 5)), np.zeros(2))
    with pytest.raises(DimensionMismatch):
        validate_problem(p)


def test_P_not_square_raises() -> None:
    p = _good()
    p = QPProblem(np.zeros((2, 3)), p.q, p.A, p.b, p.G, p.h)
    with pytest.raises(DimensionMismatch):
        validate_problem(p)


def test_P_asymmetric_raises() -> None:
    p = _good()
    P = np.array([[1.0, 0.5], [0.0, 1.0]])
    p = QPProblem(P, p.q, p.A, p.b, p.G, p.h)
    with pytest.raises(NonConvexProblem):
        validate_problem(p)


def test_P_indefinite_raises() -> None:
    p = _good()
    P = np.array([[1.0, 0.0], [0.0, -1.0]])
    p = QPProblem(P, p.q, p.A, p.b, p.G, p.h)
    with pytest.raises(NonConvexProblem):
        validate_problem(p)


def test_P_semidefinite_ok() -> None:
    p = _good()
    P = np.array([[1.0, 0.0], [0.0, 0.0]])
    p = QPProblem(P, p.q, p.A, p.b, p.G, p.h)
    validate_problem(p)
