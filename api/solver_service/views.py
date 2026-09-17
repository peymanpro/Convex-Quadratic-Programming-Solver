"""DRF views for the QP solver API."""

from __future__ import annotations

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from solver import (
    DimensionMismatch,
    InvalidProblem,
    NonConvexProblem,
    NumericalFailure,
    __version__,
)
from solver_service.serializers import (
    QPProblemSerializer,
    SolveResultSerializer,
)
from solver_service.services import solve_from_payload

EXAMPLES = [
    {
        "name": "halfplane",
        "description": "2D QP with one inequality constraint",
        "payload": {
            "P": [[1.0, 0.0], [0.0, 1.0]],
            "q": [-2.0, -3.0],
            "A": [],
            "b": [],
            "G": [[1.0, 1.0]],
            "h": [2.0],
        },
    },
    {
        "name": "equality",
        "description": "2D QP with an equality constraint",
        "payload": {
            "P": [[1.0, 0.0], [0.0, 1.0]],
            "q": [0.0, 0.0],
            "A": [[1.0, 1.0]],
            "b": [1.0],
            "G": [],
            "h": [],
        },
    },
]


@extend_schema(
    responses={
        200: inline_serializer(
            name="HealthResponse",
            fields={"status": drf_serializers.CharField()},
        )
    }
)
class HealthView(APIView):
    authentication_classes: list[str] = []
    permission_classes: list[str] = []

    def get(self, request: Request) -> Response:
        return Response({"status": "ok"})


@extend_schema(
    responses={
        200: inline_serializer(
            name="VersionResponse",
            fields={"version": drf_serializers.CharField()},
        )
    }
)
class VersionView(APIView):
    authentication_classes: list[str] = []
    permission_classes: list[str] = []

    def get(self, request: Request) -> Response:
        return Response({"version": __version__})


@extend_schema(
    responses={
        200: inline_serializer(
            name="ExamplesResponse",
            fields={"examples": drf_serializers.ListField()},
        )
    }
)
class ExamplesView(APIView):
    authentication_classes: list[str] = []
    permission_classes: list[str] = []

    def get(self, request: Request) -> Response:
        return Response({"examples": EXAMPLES})


@extend_schema(
    request=QPProblemSerializer,
    responses={200: SolveResultSerializer},
    description=("Solve a convex QP: min 0.5 x^T P x + q^T x s.t. A x = b, G x <= h."),
)
class SolveQPView(APIView):
    authentication_classes: list[str] = []
    permission_classes: list[str] = []

    def post(self, request: Request) -> Response:
        serializer = QPProblemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            result = solve_from_payload(data)
        except (InvalidProblem, NonConvexProblem, DimensionMismatch) as exc:
            return Response(
                {"error": type(exc).__name__, "detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NumericalFailure as exc:
            return Response(
                {"error": "NumericalFailure", "detail": str(exc)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        out = SolveResultSerializer(result)
        return Response(out.data, status=status.HTTP_200_OK)
