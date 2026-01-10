from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PACKAGE_ROOT.parent.parent
LOG_FILE = REPO_ROOT / "autometabuilder.log"
