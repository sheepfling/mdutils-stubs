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
python tests/test_api_coverage.py --stub-root "$PWD/mdutils-stubs"
scripts/check-typing-fixtures.sh
python tests/runtime_api.py
stubtest --allowlist stubtest-allowlist.txt mdutils
twine check dist/*
```

The wheel is installed into the consumer environment before type checking. The
API inventory checks module exports, declaration shape, call signatures,
attributes, and enum members against the pinned runtime. The positive fixture
imports all package exports; the negative fixture must produce six expected
diagnostics from both checkers. Runtime behavior tests cover aliases, selected
signatures, file writes, table alignment with `None`, marker replacement, and
methods whose runtime return is `None`. Structural checks complement semantic
consumer fixtures; they do not prove that every annotation captures every
runtime behavior.

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

## Publication gate

Before publishing either `mdutils-stubs` or `snakemd-stubs`, require both
repositories to clear the approved Alphus scan at its currently verified
version. The portable Alphus runner and version are not available in this
checkout yet, so that clearance remains pending. This package's release stays
blocked until the existing runner is identified and both results are recorded.

## Attribution and license

These declarations describe the public API of the MIT-licensed
[didix21/mdutils](https://github.com/didix21/mdutils), specifically its
[`v1.8.1` source](https://github.com/didix21/mdutils/tree/v1.8.1). The stub
package does not copy the upstream runtime implementation. See [LICENSE](LICENSE).
