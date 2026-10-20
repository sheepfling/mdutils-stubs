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

The tests package is repository tooling and is not installed in the stub wheel.
The API audit compares the checked-out stubs with the installed pinned runtime;
the consumer type checkers therefore see the installed wheel. See
[API-COVERAGE.md](API-COVERAGE.md) for the limits and compatibility procedure.

## Optional side validation

[quality-gates.toml](quality-gates.toml) contains optional local Alphus and
Markdown profiles. Those source and Markdown profiles remain advisory. The shared build, API,
and example-verification tooling is described below.

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
python -m alphus_stub_quality.verify --root . --config stub-quality.json --with-twine
```

For an unpublished local candidate, install its built Alphus wheel instead of
the Git requirement. The consumer wheel has no Alphus runtime dependency.
Python 3.10 matrix jobs can use a reviewed source checkout via
`PYTHONPATH=/path/to/alphus/src`, with the same tool dependencies provisioned.
The main Alphus CLI still requires Python 3.11 or later.
