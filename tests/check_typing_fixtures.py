"""Run mdutils's configured consumer fixtures through Alphus's supported CLI."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sysconfig
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class VerificationSettings(BaseModel):
    """Typed settings used by the repository's fixture adapter."""

    model_config = ConfigDict(extra="ignore")

    positive_fixture: str
    negative_fixture: str
    typing_checkers: tuple[str, ...] = Field(default=("mypy", "pyright"), min_length=1)
    negative_expected_count: int | None = None
    mypy_diagnostics: tuple[str, ...] = ()
    pyright_diagnostics: tuple[str, ...] = ()


class StubQualityConfig(BaseModel):
    """Validate the repository config envelope before reading fixture settings."""

    model_config = ConfigDict(extra="ignore")

    verification: VerificationSettings


def _typing_cli() -> Path:
    """Find the installed Alphus command in this interpreter's scripts directory."""
    scripts_directory = sysconfig.get_path("scripts")
    if scripts_directory is None:
        raise FileNotFoundError("Python did not report a scripts directory")
    executable = shutil.which("alphus-typing-fixtures", path=scripts_directory)
    if executable is None:
        raise FileNotFoundError(
            f"alphus-typing-fixtures is missing from {scripts_directory}; "
            "install the Alphus development tools "
            "from requirements-quality.txt"
        )
    return Path(executable)


def _settings(root: Path) -> VerificationSettings:
    config_text = (root / "stub-quality.json").read_text(encoding="utf-8")
    return StubQualityConfig.model_validate_json(config_text).verification


def _command(root: Path, settings: VerificationSettings) -> list[str]:
    command = [
        str(_typing_cli()),
        "--root",
        str(root),
        "--positive-fixture",
        str((root / settings.positive_fixture).resolve()),
        "--negative-fixture",
        str((root / settings.negative_fixture).resolve()),
        "--checkers",
        *settings.typing_checkers,
    ]
    expected_count = settings.negative_expected_count
    if expected_count is not None:
        command.extend(("--expected-count", str(expected_count)))
    for checker in ("mypy", "pyright"):
        for diagnostic in getattr(settings, f"{checker}_diagnostics"):
            command.extend((f"--{checker}-diagnostic", diagnostic))
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    root = parser.parse_args().root.expanduser().resolve()
    try:
        command = _command(root, _settings(root))
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))
    return subprocess.run(command, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
