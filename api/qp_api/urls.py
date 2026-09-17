"""Project URL configuration."""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("solver_service.urls")),
]
