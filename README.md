# mdutils-stubs

PEP 561 stubs for [mdutils](https://github.com/didix21/mdutils), a Python
library for generating Markdown files.

## Compatibility

The supported runtime baseline is exactly mdutils 1.8.1. The distribution pins
that runtime version and declares Python >=3.10,<4.0. No compatibility with
other mdutils releases is implied.

The stubs describe the public package surface and preserve package exports and
aliases. See [API coverage](API-COVERAGE.md) for the audit scope and reproducible
checks.

## List items

MDList, MDCheckbox, MdUtils.new_list, and MdUtils.new_checkbox_list accept
string leaves and recursively nested lists. Formatting, link, and image helpers
return strings, so their results can be used as list items. Arbitrary non-string
objects are outside the supported contract.

```python
from mdutils import MdUtils, TextUtils
from mdutils.tools.Image import Image
from mdutils.tools.Link import Inline

items = [
    TextUtils.bold("Important"),
    Inline.new_link("https://example.com", text="docs"),
    Image.new_inline_image("diagram", "diagram.png"),
]
MdUtils("out").new_list(items)
```

Runtime and type-checking fixtures verify these helper-generated list entries.

## Installation

```shell
python -m pip install mdutils-stubs
```

The stub distribution installs alongside mdutils and is discovered automatically
by mypy and Pyright. It is a complete stub-only distribution, so it does not
include a py.typed marker.

## Local checks

Use a Python 3.11+ verification environment. From the repository root, install
the development tools, pinned Alphus tooling and runtime, then build and install
the wheel before running the consumer checks:

```shell
python -m pip install ".[dev]" -r requirements/compatibility.txt
python -m pip install -r requirements-quality.txt
SETUPTOOLS_SCM_PRETEND_VERSION=1.8.1.0 python -m build
python -m pip install --no-deps --force-reinstall dist/mdutils_stubs-*.whl
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
python -m tests.check_typing_fixtures --root .
python -m tests.runtime_api
python -m mypy.stubtest --allowlist stubtest-allowlist.txt mdutils
python -m twine check dist/*
```

The Python fixture entry point reads stub-quality.json and delegates to
Alphus's installed alphus-typing-fixtures CLI.

The tests package is repository tooling and is not installed in the stub wheel.
The API audit compares the checked-out stubs with the installed pinned runtime;
the consumer type checkers therefore see the installed wheel. See
[API-COVERAGE.md](API-COVERAGE.md) for the limits and compatibility procedure.

## Source policy selection

[quality-gates.toml](quality-gates.toml) retains the optional `stub-package`
source-policy profile. The default `check` profile runs the stub verifier,
native Python lint/format checks, and native Markdown checks; any failing stage
fails that selection. The shared verification tooling is described below.

## Maintenance

Review each proposed mdutils version change against its public source and run
the local API, typing, runtime, and packaging checks before widening the
compatibility pin. A dependency update by itself does not establish stub
compatibility.

There is no package publication job. Merging or publishing remains a separate
release decision.

## Attribution and license

These declarations describe the public API of MIT-licensed
[didix21/mdutils](https://github.com/didix21/mdutils). The stub package does not
copy the upstream runtime implementation. See [LICENSE](LICENSE).

### Shared verification tooling

The reusable example runner and AST/API assertions come from the reviewed
Alphus revision recorded in `requirements-quality.txt`. Install that tooling
in a dedicated Python 3.11+ verification environment:

```shell
python -m pip install -r requirements-quality.txt
alphus-stub-quality --root . --config stub-quality.json --with-twine
```

For an unpublished local candidate, install its built Alphus wheel instead of
the Git requirement. The consumer wheel has no Alphus runtime dependency.
Alphus and native Mypy/Pyright run in a Python 3.11+ checker environment.
Build/install, API audit, native stubtest and smoke execute in a distinct target
venv. The target does not install Alphus. For example, after provisioning the
checker as above, use a Python 3.10 target:

```shell
python3.10 -m venv /path/to/target
/path/to/target/bin/python -m pip install -r requirements-target.txt \
  -r requirements/compatibility.txt
alphus-stub-quality --root . --config stub-quality.json \
  --with-twine --target-python /path/to/target/bin/python --report target-result.json
```

Repeat with each Python target 3.10–3.14. Both native static checkers explicitly
select that target's packages and language version; the JSON report records
checker/target identities and each executed stage. Failed target checks stop the
run without falling back to the checker.

### Consumer profiles

The `check` profile composes `stubs`, `python`, and `markdown`. Run the complete
selection with the installed pinned Alphus tooling:

```shell
alphus --root . --config quality-gates.toml --run --profile check
```

Use `--profile stubs`, `--profile python`, or `--profile markdown` to run one
part. The stub stage builds and installs the wheel before later tooling runs.
Hosted CI runs `quality` (`python` plus `markdown`) once and the shared
`ci/stub-quality` action once per target 3.10–3.14, using checker Python 3.12.
It runs only after a merged PR or manual dispatch. Both action references and
`requirements-quality.txt` pin the same immutable Alphus commit. Each
repository retains its native tool settings, examples and API expectations;
Alphus owns the repeated checking mechanisms and their regression tests.
The API adapter tests run in the stub stage; the aggregate does not repeat them
through pytest. Direct pytest remains available for working on that adapter.
