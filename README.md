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

From the repository root, install the local tools and exact target runtime
from the `dev` and `target` dependency groups, then build and install the wheel:

```shell
python -m pip install --upgrade pip
python -m pip install --group dev --group target
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

The Python fixture entry point reads stub-quality.json and invokes native MyPy
and Pyright modules without shell commands or Alphus. It checks the positive
fixture and requires every expected negative diagnostic to remain present.

The tests package is repository tooling and is not installed in the stub wheel.
The optional Alphus profile runs the structural API audit against the installed
pinned runtime; the native CI suite does not import that audit. See
[API-COVERAGE.md](API-COVERAGE.md) for the limits and compatibility procedure.

## Source policy selection

[quality-gates.toml](quality-gates.toml) retains the optional `stub-package`
source-policy profile. The default `check` profile runs the stub verifier,
native Python lint/format checks, and native Markdown checks; any failing stage
fails that selection. The `stub-package` profile is excluded from the default
selection.

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

### Optional Alphus verification

Alphus is a development-only verifier in the `local-alphus` dependency group; it
is not installed by consumers of `mdutils-stubs`. Its setup, target-environment
commands and profile selection are documented in
[ALPHUS-VERIFICATION.md](docs/ALPHUS-VERIFICATION.md).

The hosted workflow does not install or call Alphus until it is published on
PyPI. Its native checks run on Python targets 3.10–3.15, including the installed
wheel, positive and expected-negative typing fixtures, pytest runtime probe,
native stubtest, and package build. Python 3.15 is included as a compatibility
target; it does not change the declared support metadata or establish a local
3.15 result.
