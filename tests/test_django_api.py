"""Phase 13 tests: Django REST API integration."""

from __future__ import annotations

import json

import pytest
from django.test import Client


@pytest.mark.django_db
def test_health_endpoint() -> None:
    c = Client()
    r = c.get("/api/v1/health/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.django_db
def test_version_endpoint() -> None:
    c = Client()
    r = c.get("/api/v1/version/")
    assert r.status_code == 200
    assert "version" in r.json()


@pytest.mark.django_db
def test_examples_endpoint() -> None:
    c = Client()
    r = c.get("/api/v1/examples/")
    assert r.status_code == 200
    assert len(r.json()["examples"]) >= 2


@pytest.mark.django_db
def test_solve_halfplane() -> None:
    c = Client()
    payload = {
        "P": [[1.0, 0.0], [0.0, 1.0]],
        "q": [-2.0, -3.0],
        "G": [[1.0, 1.0]],
        "h": [2.0],
    }
    r = c.post(
        "/api/v1/solve/qp/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "optimal"
    assert abs(body["x"][0] - 0.5) <= 1e-4
    assert abs(body["x"][1] - 1.5) <= 1e-4


@pytest.mark.django_db
def test_solve_nonconvex_returns_400() -> None:
    c = Client()
    payload = {"P": [[1.0, 0.0], [0.0, -1.0]], "q": [0.0, 0.0]}
    r = c.post(
        "/api/v1/solve/qp/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert r.status_code == 400
    assert r.json()["error"] == "NonConvexProblem"


@pytest.mark.django_db
def test_solve_dimension_mismatch_returns_400() -> None:
    c = Client()
    payload = {"P": [[1.0, 0.0], [0.0, 1.0]], "q": [0.0, 0.0, 0.0]}
    r = c.post(
        "/api/v1/solve/qp/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert r.status_code == 400
