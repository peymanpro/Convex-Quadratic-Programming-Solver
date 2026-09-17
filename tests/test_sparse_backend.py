"""Tests for the sparse backend via public API."""

from __future__ import annotations

import numpy as np

from solver import IPMOptions, QPProblem, solve


def _halfplane() -> QPProblem:
    return QPProblem(
        P=np.eye(2),
        q=np.array([-2.0, -3.0]),
        A=np.zeros((0, 2)),
        b=np.zeros(0),
        G=np.array([[1.0, 1.0]]),
        h=np.array([2.0]),
    )


def test_sparse_backend_mehrotra() -> None:
    r = solve(_halfplane(), backend="sparse")
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([0.5, 1.5]), atol=1e-4)


def test_sparse_backend_ipm() -> None:
    r = solve(_halfplane(), method="ipm", backend="sparse")
    assert r.status == "optimal"
    assert np.allclose(r.x, np.array([0.5, 1.5]), atol=1e-4)


def test_sparse_matches_dense() -> None:
    r_d = solve(_halfplane(), backend="dense")
    r_s = solve(_halfplane(), backend="sparse")
    assert r_d.status == "optimal"
    assert r_s.status == "optimal"
    assert np.allclose(r_d.x, r_s.x, atol=1e-6)
    assert abs(r_d.objective - r_s.objective) <= 1e-6


def test_sparse_option_override() -> None:
    opts = IPMOptions(backend="sparse")
    r = solve(_halfplane(), options=opts)
    assert r.status == "optimal"
