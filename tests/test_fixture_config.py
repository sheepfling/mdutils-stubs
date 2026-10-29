"""Validation tests for the native typing-fixture configuration."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from tests.check_typing_fixtures import FixtureConfig, _parse_config


def _document() -> dict[str, object]:
    return {
        "verification": {
            "positive_fixture": "tests/fixtures/positive.py",
            "negative_fixture": "tests/fixtures/negative.py",
            "typing_checkers": ["mypy", "pyright"],
            "negative_expected_count": 7,
            "mypy_diagnostics": ['Argument "file_name"'],
            "pyright_diagnostics": ['parameter "file_name"'],
        }
    }


def test_parse_config_returns_validated_fixture_config() -> None:
    config = _parse_config(_document())

    assert isinstance(config, FixtureConfig)
    assert config.positive_fixture == Path("tests/fixtures/positive.py")
    assert config.negative_fixture == Path("tests/fixtures/negative.py")
    assert config.typing_checkers == ("mypy", "pyright")
    assert config.negative_expected_count == 7
    assert config.mypy_diagnostics == ('Argument "file_name"',)
    assert config.pyright_diagnostics == ('parameter "file_name"',)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("positive_fixture", "", "non-empty relative path"),
        ("negative_fixture", "/tmp/negative.py", "stay inside the repository"),
        ("negative_fixture", "../negative.py", "stay inside the repository"),
        ("typing_checkers", ["mypy", "mypy"], "once each"),
        ("typing_checkers", ["other"], "mypy and/or pyright"),
        ("negative_expected_count", True, "positive integer"),
        ("mypy_diagnostics", [1], "list of strings"),
    ],
)
def test_parse_config_rejects_invalid_values(field: str, value: object, message: str) -> None:
    document = _document()
    verification = cast(dict[str, object], document["verification"])
    verification[field] = value

    with pytest.raises(ValueError, match=message):
        _parse_config(document)
