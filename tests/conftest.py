"""Pytest configuration to enable Django."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "api"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qp_api.settings")
