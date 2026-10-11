"""Run positive and negative consumer typing checks without a shell."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(".")
POSITIVE_FIXTURE = ROOT / "tests" / "fixtures" / "positive.py"
NEGATIVE_FIXTURE = ROOT / "tests" / "fixtures" / "negative.py"
EXPECTED_ERROR_COUNT = 7
ERROR_LINE = re.compile(r"\berror:\s")


@dataclass(frozen=True, slots=True)
class Checker:
    name: str
    module: str
    negative_diagnostics: tuple[str, ...]


CHECKERS = (
    Checker(
        "mypy",
        "mypy",
        (
            'Argument "file_name"',
            'Argument "level"',
            'Argument "title"',
            "List item 0",
            'Argument "text_align"',
            "list[_ListItem]",
            'Argument "text"',
        ),
    ),
    Checker(
        "pyright",
        "pyright",
        (
            'parameter "file_name"',
            'parameter "level"',
            'parameter "title"',
            'parameter "text" of type "list[str]"',
            'parameter "text_align"',
            'parameter "items" of type "list[_ListItem]"',
            'parameter "text" of type "str"',
        ),
    ),
)

ProcessRunner = Callable[..., subprocess.CompletedProcess[str]]


def build_command(
    checker: Checker, fixture: Path, cache_directory: Path | None = None
) -> list[str]:
    """Build an argv vector using this interpreter and no shell wrapper."""
    command = [sys.executable, "-m", checker.module]
    if checker.name == "mypy":
        if cache_directory is None:
            raise ValueError("mypy requires a temporary cache directory")
        command.extend(("--strict", "--cache-dir", str(cache_directory)))
    elif checker.name == "pyright":
        command.extend(("--pythonpath", sys.executable))
    else:
        raise ValueError(f"unknown checker: {checker.name}")
    command.append(str(fixture.resolve()))
    return command


def evaluate_result(
    checker: Checker,
    fixture: Path,
    result: subprocess.CompletedProcess[str],
    *,
    expect_errors: bool,
) -> list[str]:
    """Return contract violations for a checker process result."""
    output = "\n".join(part for part in (result.stdout, result.stderr) if part)
    error_lines = [line for line in output.splitlines() if ERROR_LINE.search(line)]
    issues: list[str] = []

    if not expect_errors:
        if result.returncode != 0:
            issues.append(f"expected exit 0, got {result.returncode}")
        if error_lines:
            issues.append(f"expected no diagnostics, got {len(error_lines)} error lines")
        return issues

    if result.returncode == 0:
        issues.append("negative fixture unexpectedly passed")
    if len(error_lines) != EXPECTED_ERROR_COUNT:
        issues.append(f"expected {EXPECTED_ERROR_COUNT} error diagnostics, got {len(error_lines)}")
    missing = [
        diagnostic for diagnostic in checker.negative_diagnostics if diagnostic not in output
    ]
    if missing:
        issues.append("missing expected diagnostics: " + "; ".join(missing))
    return issues


def _text_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _report_failure(
    checker: Checker,
    fixture: Path,
    command: Sequence[str],
    reason: str,
    output: str = "",
    returncode: int | None = None,
) -> None:
    print(f"FAIL {checker.name} {fixture.name}: {reason}", file=sys.stderr)
    print(f"  command: {command!r}", file=sys.stderr)
    if returncode is not None:
        print(f"  exit code: {returncode}", file=sys.stderr)
    if output:
        print("  output:", file=sys.stderr)
        print(output.rstrip(), file=sys.stderr)


def run_case(
    checker: Checker,
    fixture: Path,
    *,
    expect_errors: bool,
    process_runner: ProcessRunner | None = None,
) -> bool:
    """Run one fixture and check its exit status and diagnostic contract."""
    runner = subprocess.run if process_runner is None else process_runner

    def invoke(cache_directory: Path | None) -> bool:
        command = build_command(checker, fixture, cache_directory)
        try:
            result = runner(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=180,
            )
        except subprocess.TimeoutExpired as error:
            output = "\n".join(
                part for part in (_text_output(error.stdout), _text_output(error.stderr)) if part
            )
            _report_failure(checker, fixture, command, "timed out after 180 seconds", output)
            return False
        except OSError as error:
            _report_failure(checker, fixture, command, f"could not start checker: {error}")
            return False

        issues = evaluate_result(checker, fixture, result, expect_errors=expect_errors)
        if issues:
            output = "\n".join(part for part in (result.stdout, result.stderr) if part)
            _report_failure(
                checker,
                fixture,
                command,
                "; ".join(issues),
                output,
                result.returncode,
            )
            return False

        expectation = f"{EXPECTED_ERROR_COUNT} expected errors" if expect_errors else "clean"
        print(f"PASS {checker.name} {fixture.name}: {expectation}")
        return True

    if checker.name == "mypy":
        with tempfile.TemporaryDirectory(prefix="mdutils-stubs-mypy-") as cache:
            return invoke(Path(cache))
    return invoke(None)


def main() -> int:
    """Run all eight positive/negative checker cases."""
    success = True
    for checker in CHECKERS:
        success = run_case(checker, POSITIVE_FIXTURE, expect_errors=False) and success
        success = run_case(checker, NEGATIVE_FIXTURE, expect_errors=True) and success
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
