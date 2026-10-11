# mdutils-stubs

PEP 561 type stubs for [mdutils](https://github.com/didix21/mdutils), a Python
library for generating Markdown files.

## Supported versions

The initial candidate targets exactly **mdutils 1.8.1** and Python
**3.10–3.14**. The runtime dependency is pinned to `mdutils==1.8.1`; no wider
runtime range is claimed. The version format follows
`RUNTIME_MAJOR.RUNTIME_MINOR.RUNTIME_PATCH.STUB_REV`, so the first tag is
`v1.8.1.0`. Versions are derived from Git tags with `setuptools-scm`.

| mdutils version | Status | Evidence |
| --- | --- | --- |
| 1.8.1 | Initial supported baseline | Runtime source signatures and consumer fixtures |
| 1.8.0 | Not supported yet | Signatures match 1.8.1; full installed-wheel checks remain required before widening |
| 1.8.2 and later | Not supported yet | Review and test each upstream release before changing the dependency bound |

The distribution metadata declares Python `>=3.10,<4.0`, with classifiers
through Python 3.14. Mypy and Pyright accepted the positive fixture for targets
3.10–3.14. The installed runtime and stub wheels passed API-inventory and
runtime checks on Python 3.10.22, 3.11.16, 3.12.14, 3.13.15, and 3.14.7.
Python 3.10 also passed the seven expected positive/negative consumer checks
and strict stubtest against all 13 modules.

The stubs cover the public package exports and classes listed in
[API-COVERAGE.md](API-COVERAGE.md). They are based on the upstream 1.8.1 source
tag at commit `170f7d040ea598672c53015a5db4fab868dacba0`, including its
package-level re-exports. In that release, `mdutils.TextUtils` is the
`TextUtils` class; `MdUtils.textUtils` stores that class object.

## Installation

```shell
python -m pip install mdutils-stubs
```

The stub distribution installs alongside the runtime package and is discovered
automatically by mypy and Pyright. This is a complete stub-only distribution,
so it does not include a `py.typed` marker.

## Local checks

Use Python 3.12 for the current quality baseline. In a clean environment, install
the package and development tools, then run:

```shell
python -m pip install ".[dev]" -r requirements/compatibility.txt
SETUPTOOLS_SCM_PRETEND_VERSION=1.8.1.0 python -m build
python -m pip install --no-deps --force-reinstall dist/mdutils_stubs-*.whl
ruff check .
ruff format --check .
python tests/test_typing_fixture_runner.py
python tests/test_api_coverage.py --stub-root "$PWD/mdutils-stubs"
python scripts/check_typing_fixtures.py
python tests/runtime_api.py
stubtest --allowlist stubtest-allowlist.txt mdutils
twine check dist/*
```

The wheel is installed into the consumer environment before type checking. The
API inventory checks module exports, declaration shape, callable signatures,
annotations, attributes, and enum members against the pinned runtime. The
positive fixture imports all package exports and calls every public callable;
the negative fixture must produce seven expected diagnostics from both checkers,
including rejection of a non-string nested-list item.

Runtime behavior tests include recursive list and TOC inputs, aliases, file
writes, table alignment with `None`, marker replacement, and methods whose
runtime return is `None`. Structural checks complement semantic consumer
fixtures; they do not prove that every annotation captures every runtime
behavior.

The full aggregate runs in a clean Python 3.12 environment; the separate matrix
above records the actual interpreter versions checked with installed wheels.

## Optional repository quality profiles

The repository keeps portable Alphus policy in
[`quality-gates.toml`](quality-gates.toml). Alphus is pinned to source commit
`73e4cdb529a2945acac0c61941bf296ccb368880` of
[`sheepfling/alphus`](https://github.com/sheepfling/alphus) (version `0.1.0`);
install that immutable revision in a Python 3.11+ environment before running
the profile. Install this checkout's package and development tools into that same
environment so the profile has mdutils, the stubs, Mypy, and Pyright:

```shell
python -m pip install \
  "alphus @ git+https://github.com/sheepfling/alphus.git@73e4cdb529a2945acac0c61941bf296ccb368880"
python -m pip install ".[dev]"
alphus --root . --config quality-gates.toml --run --profile stub-package
```

The independent `markdown-quality` profile invokes `mdrepo 0.0.1.post0` for
Markdown link/graph checks and `rumdl 0.2.77` for Markdown lint. Those tools are
optional external commands, not package dependencies or hosted CI jobs. The
profile disables rumdl's line-length rule because the Alphus policy owns those
limits. It enables mdrepo's document graph from `README.md` without copying
either tool's validation logic into this repository.

```shell
alphus --root . --config quality-gates.toml --run --profile markdown-quality
```

## Maintenance

The candidate includes Dependabot configuration for a weekly check of the exact
`mdutils` compatibility pin, with at most one version-update pull request open.
Scheduled checks begin only after GitHub accepts this configuration in the
repository. A Dependabot update only proposes a runtime version change; it does
not update the stubs or establish compatibility. Before accepting a runtime
bump, compare the upstream public API and run the full local gate against a clean
wheel install, including mypy, Pyright, stubtest, runtime checks, and wheel/sdist
validation. Update the supported version table and dependency bound only after
those checks pass.

The candidate defines one lightweight verification workflow after a pull
request is merged, plus manual dispatch. Local checks are the pre-merge gate.
There is no push-triggered or pull-request-opened workflow and no package
publication job.

## Release gate

The Alphus `stub-package` and optional `markdown-quality` profiles are local
release gates; both passed during this candidate's verification. A local pass
is evidence for this repository only; it does not authorize publication or
establish SnakeMD status. No package publication is performed by this project.

## Attribution and license

These declarations describe the public API of the MIT-licensed
[didix21/mdutils](https://github.com/didix21/mdutils), specifically its
[`v1.8.1` source](https://github.com/didix21/mdutils/tree/v1.8.1). The stub
package does not copy the upstream runtime implementation. See [LICENSE](LICENSE).
