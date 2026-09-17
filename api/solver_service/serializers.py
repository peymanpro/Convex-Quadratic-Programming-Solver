"""DRF serializers for the QP solver API."""

from __future__ import annotations

from typing import Any

from rest_framework import serializers


class ArrayField(serializers.ListField):
    child = serializers.FloatField()


class MatrixField(serializers.ListField):
    child = ArrayField()


class QPProblemSerializer(serializers.Serializer):
    P = MatrixField()
    q = ArrayField()
    A = MatrixField(required=False, default=list)
    b = ArrayField(required=False, default=list)
    G = MatrixField(required=False, default=list)
    h = ArrayField(required=False, default=list)
    method = serializers.ChoiceField(
        choices=["mehrotra", "ipm"], required=False, default="mehrotra"
    )
    tol = serializers.FloatField(required=False, default=1e-8)
    max_iter = serializers.IntegerField(required=False, default=200)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if not attrs["P"]:
            raise serializers.ValidationError("P must not be empty.")
        if not attrs["q"]:
            raise serializers.ValidationError("q must not be empty.")
        return attrs


class SolveResultSerializer(serializers.Serializer):
    status = serializers.CharField()
    x = ArrayField()
    objective = serializers.FloatField()
    iterations = serializers.IntegerField()
    primal_residual = serializers.FloatField()
    dual_residual = serializers.FloatField()
    duality_gap = serializers.FloatField()
    solve_time = serializers.FloatField()
