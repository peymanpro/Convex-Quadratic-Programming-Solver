"""URL routing for solver_service."""

from __future__ import annotations

from django.urls import path

from solver_service.views import (
    ExamplesView,
    HealthView,
    SolveQPView,
    VersionView,
)

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("version/", VersionView.as_view(), name="version"),
    path("examples/", ExamplesView.as_view(), name="examples"),
    path("solve/qp/", SolveQPView.as_view(), name="solve-qp"),
]
