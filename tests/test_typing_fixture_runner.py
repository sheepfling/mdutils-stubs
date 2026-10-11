"""Portability tests for the typing-fixture subprocess runner."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from collections.abc import Sequence
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(".")
RUNNER_PATH = ROOT / "scripts" / "check_typing_fixtures.py"
SPEC = importlib.util.spec_from_file_location("check_typing_fixtures", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import typing-fixture runner from {RUNNER_PATH}")
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


class TypingFixtureRunnerTests(unittest.TestCase):
    def test_commands_use_python_modules_and_argument_vectors(self) -> None:
        mypy_command = runner.build_command(
            runner.CHECKERS[0], runner.POSITIVE_FIXTURE, Path("/tmp/mypy-cache")
        )
        pyright_command = runner.build_command(runner.CHECKERS[1], runner.POSITIVE_FIXTURE)

        self.assertEqual(mypy_command[:3], [sys.executable, "-m", "mypy"])
        self.assertEqual(pyright_command[:3], [sys.executable, "-m", "pyright"])
        self.assertIn("--pythonpath", pyright_command)
        self.assertEqual(pyright_command[pyright_command.index("--pythonpath") + 1], sys.executable)
        self.assertTrue(all(isinstance(argument, str) for argument in mypy_command))
        self.assertTrue(all(isinstance(argument, str) for argument in pyright_command))

    def test_mypy_cache_is_temporary_and_process_uses_no_shell(self) -> None:
        cache_paths: list[Path] = []

        def fake_run(command: Sequence[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            cache = Path(command[command.index("--cache-dir") + 1])
            self.assertTrue(cache.is_dir())
            self.assertEqual(kwargs["cwd"], ROOT)
            self.assertNotIn("shell", kwargs)
            cache_paths.append(cache)
            return subprocess.CompletedProcess(command, 0, "Success: no issues found", "")

        output = StringIO()
        with patch.object(runner.subprocess, "run", side_effect=fake_run):
            with redirect_stdout(output):
                self.assertTrue(
                    runner.run_case(
                        runner.CHECKERS[0],
                        runner.POSITIVE_FIXTURE,
                        expect_errors=False,
                    )
                )

        self.assertEqual(len(cache_paths), 1)
        self.assertFalse(cache_paths[0].exists())
        self.assertIn("PASS mypy", output.getvalue())

    def test_negative_contract_requires_seven_errors_and_each_expected_message(self) -> None:
        for checker in runner.CHECKERS:
            with self.subTest(checker=checker.name):
                output = "\n".join(
                    f"fixture.py:{index}: error: {diagnostic} has wrong type"
                    for index, diagnostic in enumerate(checker.negative_diagnostics, start=1)
                )
                passed = subprocess.CompletedProcess([], 1, output, "")
                failed_count = subprocess.CompletedProcess([], 1, output.splitlines()[0], "")
                failed_status = subprocess.CompletedProcess([], 0, "", "")

                self.assertEqual(
                    runner.evaluate_result(
                        checker, runner.NEGATIVE_FIXTURE, passed, expect_errors=True
                    ),
                    [],
                )
                self.assertTrue(
                    runner.evaluate_result(
                        checker, runner.NEGATIVE_FIXTURE, failed_count, expect_errors=True
                    )
                )
                self.assertTrue(
                    runner.evaluate_result(
                        checker, runner.NEGATIVE_FIXTURE, failed_status, expect_errors=True
                    )
                )

    def test_spawn_failure_is_reported_and_mypy_cache_is_cleaned(self) -> None:
        cache_paths: list[Path] = []

        def failing_run(
            command: Sequence[str], **kwargs: object
        ) -> subprocess.CompletedProcess[str]:
            cache = Path(command[command.index("--cache-dir") + 1])
            self.assertTrue(cache.is_dir())
            cache_paths.append(cache)
            raise OSError("simulated missing interpreter")

        errors = StringIO()
        with patch.object(runner.subprocess, "run", side_effect=failing_run):
            with redirect_stderr(errors):
                self.assertFalse(
                    runner.run_case(
                        runner.CHECKERS[0],
                        runner.POSITIVE_FIXTURE,
                        expect_errors=False,
                    )
                )

        self.assertEqual(len(cache_paths), 1)
        self.assertFalse(cache_paths[0].exists())
        self.assertIn("could not start checker", errors.getvalue())
        self.assertIn("simulated missing interpreter", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
