# Optional Alphus verification

Alphus is a maintainer-side verification tool, not a dependency of the
`mdutils-stubs` distribution. The package runtime requirement remains
`mdutils==1.8.1`. Install the pinned shared tooling only in a separate Python
3.11+ checker environment:

```sh
python -m pip install --upgrade pip
python -m pip install --group dev --group target
python -m pip install --group dev-experimental
alphus --root . --config quality-gates.toml --run --profile check
```

The Git-based install is isolated in `dev-experimental`; ordinary pip setup and
hosted CI select only `dev` and `target`. uv resolves all declared dependency
groups when creating or refreshing a lockfile, so `uv lock` may require Git
access to this experimental group. uv was not installed in the validation
environment, so no uv command was run.

The default `check` profile combines `stubs`, `python`, and `markdown`. Individual
profiles can be selected with `--profile stubs`, `--profile python`, or
`--profile markdown`. The optional source-policy scan is separate:

```sh
alphus --root . --config quality-gates.toml --run --profile stub-package
```

For installed-consumer verification, `alphus-stub-quality` builds and installs
the stub wheel in a distinct target environment while its checker and MyPy /
Pyright remain in the checker environment:

```sh
alphus-stub-quality --root . --config stub-quality.json --with-twine
```

To select another installed Python interpreter, provision it from the `target`
dependency group, then pass its path explicitly:

```sh
python -m pip install --upgrade pip
/path/to/target/bin/python -m pip install --group target
export ALPHUS_TARGET_PYTHON=/path/to/target/bin/python
alphus-stub-quality --root . --config stub-quality.json --with-twine \
  --target-python /path/to/target/bin/python --report target-result.json
```

The target environment does not install Alphus. The built stub wheel contains no
Alphus runtime dependency. Hosted CI does not install or call Alphus until it is
available on PyPI; it runs native quality, wheel, typing, pytest runtime, and
stubtest checks on Python 3.10–3.15. It runs only for merged pull requests or
manual dispatch; an ordinary pull request update does not start the workflow.
