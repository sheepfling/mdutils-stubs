"""Run mdutils's configured example contracts through Alphus."""

from pathlib import Path

from alphus_stub_quality.typing_fixtures import run_suite
from alphus_stub_quality.verify import read_config


def main() -> int:
    root = Path.cwd()
    settings = read_config(root, Path("stub-quality.json"))
    passed = run_suite(
        root / settings.positive_fixture,
        root / settings.negative_fixture,
        root=root,
        expected_count=settings.negative_expected_count,
        mypy_diagnostics=settings.mypy_diagnostics,
        pyright_diagnostics=settings.pyright_diagnostics,
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
