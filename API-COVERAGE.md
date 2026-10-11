# API coverage and compatibility

This document describes the audit contract and how to run it. The executable
tests are the source of API completeness checks; this file does not duplicate a
member-by-member snapshot or manually maintained totals.

## Supported baseline

The current runtime baseline is mdutils 1.8.1. The audit is based on the
upstream public [v1.8.1 source](https://github.com/didix21/mdutils/tree/v1.8.1),
commit 170f7d040ea598672c53015a5db4fab868dacba0. The installed runtime version
is checked against this exact baseline. Other releases are not included in the
compatibility claim.

## Audit scope

The version-specific audit manifest in tests/test_api_coverage.py identifies
runtime modules, package exports, and re-export targets. The test discovers the
actual installed runtime and compares that scope with the stub tree. It checks:

- one-to-one runtime module and stub module coverage;
- public definitions, class bases, callable names and signature shape;
- public class attributes and enum members;
- package exports and aliases against both the runtime and stubs;
- complete annotations on public stub callables; and
- typed fixture calls for the exported API.

A runtime change fails the audit until the corresponding stub and the
version-specific manifest are deliberately reviewed. The checks derive the
compared names and signatures from the installed source rather than relying on
documentation counts.

## Behavioral and consumer checks

tests/fixtures/positive.py imports package exports and exercises public
callables for mypy and Pyright. tests/fixtures/negative.py covers invalid
arguments and rejects non-string nested list leaves. The typing runner requires
both checkers to accept the positive fixture and to emit the expected
diagnostics for the negative fixture.

The runtime checks cover selected behavior such as recursive lists and tables
of contents, file operations, and helper-produced Markdown strings used as
list leaves. Strict stubtest compares an installed stub wheel with the pinned
runtime. Structural parity, typing fixtures, runtime examples, and stubtest
provide distinct evidence; together they are still not a proof of every
possible runtime behavior.

For list input, the supported leaf contract is str. MDList and MDCheckbox also
accept recursive lists of those strings. Text formatting, inline link, and
image helpers return strings, so those results satisfy the same contract.
Non-string objects are not modeled as list leaves.

## Run the audit

Run these commands from the repository root with mdutils 1.8.1 and the
development dependencies installed. Install the built wheel in the environment
before running consumer checks so import resolution exercises the distribution:

```shell
python -m pytest -q
python -m tests.check_typing_fixtures
python -m tests.runtime_api
python -m mypy.stubtest --allowlist stubtest-allowlist.txt mdutils
```

Pytest runs the API audit against the checked-out stub tree and the installed
runtime. The typing runner uses the current interpreter to invoke each checker
without a shell. The runtime module invokes the installed library and asserts
selected observable output.

## Updating the baseline

When changing the supported mdutils release, review the upstream API and source
reference, runtime dependency pin, module/export manifest, stubs, fixtures, and
runtime cases as one change. Run the installed-wheel checks on the candidate
before widening compatibility. Python support and distribution metadata remain
declared in pyproject.toml.
