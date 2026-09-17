"""DRF views for the QP solver API."""

from __future__ import annotations

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


class HealthView(APIView):
    authentication_classes: list[str] = []
    permission_classes: list[str] = []

    def get(self, request: Request) -> Response:
        return Response({"status": "ok"})


class VersionView(APIView):
    authentication_classes: list[str] = []
    permission_classes: list[str] = []

    def get(self, request: Request) -> Response:
        return Response({"version": __version__})


class ExamplesView(APIView):
    authentication_classes: list[str] = []
    permission_classes: list[str] = []

    def get(self, request: Request) -> Response:
        return Response({"examples": EXAMPLES})


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
