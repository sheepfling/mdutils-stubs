"""Include the installed-runtime consumer probe in the native pytest suite."""

from __future__ import annotations

from tests.runtime_api import main


def test_runtime_api_consumer() -> None:
    main()
