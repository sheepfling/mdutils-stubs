# Optional Alphus verification

Alphus is a maintainer-side verification tool, not a dependency of the
`mdutils-stubs` distribution. The package runtime requirement remains
`mdutils==1.8.1`. Install the pinned shared tooling only in a separate Python
3.11+ checker environment:

```sh
python -m pip install -r requirements-quality.txt
alphus --root . --config quality-gates.toml --run --profile check
```

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

To select another installed Python interpreter, provision it with
`requirements-target.txt` and `requirements/compatibility.txt`, then pass its
path explicitly:

```sh
/path/to/target/bin/python -m pip install -r requirements-target.txt \
  -r requirements/compatibility.txt
alphus-stub-quality --root . --config stub-quality.json --with-twine \
  --target-python /path/to/target/bin/python --report target-result.json
```

The target environment does not install Alphus. The built stub wheel contains no
Alphus runtime dependency. CI invokes the quality and compatibility actions only
for merged pull requests or manual dispatch; an ordinary pull request update
does not start these optional checks.
