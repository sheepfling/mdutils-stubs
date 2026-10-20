"""Supply repository-owned fixture paths from pytest's selected project root."""

from __future__ import annotations

import pytest

from tests.test_api_coverage import PublicApiCoverageTests


@pytest.fixture(scope="class", autouse=True)
def api_stub_root(request: pytest.FixtureRequest) -> None:
    if request.cls is PublicApiCoverageTests:
        PublicApiCoverageTests.stub_root = request.config.rootpath / "mdutils-stubs"
