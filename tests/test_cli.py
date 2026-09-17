"""Phase 15 tests: CLI entry point."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from solver.cli import main


def test_cli_solve(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = {
        "P": [[1.0, 0.0], [0.0, 1.0]],
        "q": [-2.0, -3.0],
        "G": [[1.0, 1.0]],
        "h": [2.0],
    }
    path = tmp_path / "qp.json"
    path.write_text(json.dumps(payload))
    rc = main([str(path)])
    captured = capsys.readouterr()
    assert rc == 0
    body = json.loads(captured.out)
    assert body["status"] == "optimal"
    assert abs(body["x"][0] - 0.5) <= 1e-4
