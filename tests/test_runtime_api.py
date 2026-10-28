"""Include the installed-runtime consumer probe in the native pytest suite."""

from __future__ import annotations

import runpy


def test_runtime_api_consumer() -> None:
    runpy.run_module("tests.runtime_api", run_name="__main__")
