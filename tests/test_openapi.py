"""Phase 14 tests: OpenAPI schema and Swagger UI."""

from __future__ import annotations

import pytest
from django.test import Client


@pytest.mark.django_db
def test_schema_endpoint() -> None:
    c = Client()
    r = c.get("/api/schema/")
    assert r.status_code == 200
    body = r.content.decode()
    assert "Convex QP Solver API" in body
    assert "/api/v1/solve/qp/" in body


@pytest.mark.django_db
def test_swagger_ui_loads() -> None:
    c = Client()
    r = c.get("/api/docs/")
    assert r.status_code == 200
    assert b"swagger" in r.content.lower()
