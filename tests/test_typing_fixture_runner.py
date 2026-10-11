"""Pytest coverage for the shell-free typing-fixture runner."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import pytest

from tests import check_typing_fixtures as runner

ROOT = Path(".")
POSITIVE = ROOT / "tests" / "fixtures" / "positive.py"
NEGATIVE = ROOT / "tests" / "fixtures" / "negative.py"


@pytest.mark.parametrize("checker", runner.CHECKERS, ids=lambda item: item.name)
def test_commands_use_this_interpreter_and_module_invocations(checker: runner.Checker) -> None:
    cache = Path("/tmp/mdutils-stubs-cache") if checker.name == "mypy" else None
    command = runner.build_command(checker, POSITIVE, cache)

    assert command[:3] == [sys.executable, "-m", checker.module]
    assert all(isinstance(argument, str) for argument in command)
    if checker.name == "pyright":
        interpreter_index = command.index("--pythonpath") + 1
        assert command[interpreter_index] == sys.executable


@pytest.mark.parametrize("checker", runner.CHECKERS, ids=lambda item: item.name)
def test_positive_contract_requires_zero_exit_and_no_errors(checker: runner.Checker) -> None:
    passed = subprocess.CompletedProcess([], 0, "Success: no issues found", "")
    failed = subprocess.CompletedProcess([], 1, "error: rejected", "")
    diagnostic = subprocess.CompletedProcess([], 0, "error: unexpected", "")

    assert runner.evaluate_result(checker, POSITIVE, passed, expect_errors=False) == []
    assert runner.evaluate_result(checker, POSITIVE, failed, expect_errors=False)
    assert runner.evaluate_result(checker, POSITIVE, diagnostic, expect_errors=False)


@pytest.mark.parametrize("checker", runner.CHECKERS, ids=lambda item: item.name)
def test_negative_contract_requires_all_seven_expected_diagnostics(
    checker: runner.Checker,
) -> None:
    output = chr(10).join(
        f"fixture.py:{index}: error: {diagnostic} has wrong type"
        for index, diagnostic in enumerate(checker.negative_diagnostics, start=1)
    )
    passed = subprocess.CompletedProcess([], 1, output, "")
    failed_count = subprocess.CompletedProcess([], 1, output.splitlines()[0], "")
    unexpected_success = subprocess.CompletedProcess([], 0, "", "")

    assert runner.evaluate_result(checker, NEGATIVE, passed, expect_errors=True) == []
    count_issues = runner.evaluate_result(checker, NEGATIVE, failed_count, expect_errors=True)
    assert any("expected 7 error diagnostics" in issue for issue in count_issues)
    assert any("missing expected diagnostics" in issue for issue in count_issues)
    status_issues = runner.evaluate_result(
        checker, NEGATIVE, unexpected_success, expect_errors=True
    )
    assert any("negative fixture unexpectedly passed" in issue for issue in status_issues)


def test_mypy_cache_is_temporary_and_subprocess_uses_no_shell(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    cache_paths: list[Path] = []

    def fake_run(command: Sequence[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        cache = Path(command[command.index("--cache-dir") + 1])
        assert cache.is_dir()
        assert kwargs["cwd"] == ROOT
        assert kwargs["encoding"] == "utf-8"
        assert "shell" not in kwargs
        cache_paths.append(cache)
        return subprocess.CompletedProcess(command, 0, "Success: no issues found", "")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.run_case(runner.CHECKERS[0], POSITIVE, expect_errors=False)
    assert len(cache_paths) == 1
    assert not cache_paths[0].exists()
    assert "PASS mypy positive.py: clean" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("failure", "expected_reason", "expected_output"),
    [
        pytest.param(
            FileNotFoundError("missing checker"),
            "could not start checker",
            None,
            id="spawn-failure",
        ),
        pytest.param(
            subprocess.TimeoutExpired(
                ["mypy"], 180, output=b"partial stdout", stderr=b"partial stderr"
            ),
            "timed out after 180 seconds",
            "partial stdout" + chr(10) + "partial stderr",
            id="timeout",
        ),
    ],
)
def test_failures_are_reported_and_temporary_cache_is_cleaned(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: OSError | subprocess.TimeoutExpired,
    expected_reason: str,
    expected_output: str | None,
) -> None:
    cache_paths: list[Path] = []

    def failing_run(command: Sequence[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        cache = Path(command[command.index("--cache-dir") + 1])
        assert cache.is_dir()
        cache_paths.append(cache)
        raise failure

    monkeypatch.setattr(runner.subprocess, "run", failing_run)
    assert not runner.run_case(runner.CHECKERS[0], POSITIVE, expect_errors=False)
    assert len(cache_paths) == 1
    assert not cache_paths[0].exists()
    report = capsys.readouterr().err
    assert expected_reason in report
    assert "command:" in report
    if expected_output is not None:
        assert expected_output in report
