"""Run mdutils's configured consumer fixtures through Alphus's supported CLI."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def _typing_cli() -> Path:
    """Locate the installed Alphus console script beside this interpreter."""
    name = "alphus-typing-fixtures.exe" if os.name == "nt" else "alphus-typing-fixtures"
    executable = Path(sys.executable).parent / name
    if not executable.is_file():
        raise FileNotFoundError(
            f"{executable} is missing; install the Alphus development tools "
            "from requirements-quality.txt"
        )
    return executable


def _settings(root: Path) -> dict[str, Any]:
    config = json.loads((root / "stub-quality.json").read_text(encoding="utf-8"))
    verification = config.get("verification")
    if not isinstance(verification, dict):
        raise ValueError("stub-quality.json must contain a verification object")
    return verification


def _command(root: Path, settings: dict[str, Any]) -> list[str]:
    checkers = settings.get("typing_checkers", ["mypy", "pyright"])
    if not isinstance(checkers, list) or not checkers:
        raise ValueError("verification.typing_checkers must be a non-empty list")
    command = [
        str(_typing_cli()),
        "--root",
        str(root),
        "--positive-fixture",
        str((root / settings["positive_fixture"]).resolve()),
        "--negative-fixture",
        str((root / settings["negative_fixture"]).resolve()),
        "--checkers",
        *checkers,
    ]
    expected_count = settings.get("negative_expected_count")
    if expected_count is not None:
        command.extend(("--expected-count", str(expected_count)))
    for checker in ("mypy", "pyright"):
        for diagnostic in settings.get(f"{checker}_diagnostics", []):
            command.extend((f"--{checker}-diagnostic", diagnostic))
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    root = parser.parse_args().root.expanduser().resolve()
    try:
        command = _command(root, _settings(root))
    except (FileNotFoundError, KeyError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    return subprocess.run(command, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
