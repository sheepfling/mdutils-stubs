#!/usr/bin/env bash
set -euo pipefail

mypy --strict tests/fixtures/positive.py
pyright tests/fixtures/positive.py

check_negative() {
    local label="$1"
    shift
    local output
    output="$(mktemp)"
    if "$@" >"$output" 2>&1; then
        cat "$output"
        rm -f "$output"
        printf '%s unexpectedly accepted the negative fixture\n' "$label" >&2
        return 1
    fi
    if ! rg -q 'error' "$output"; then
        cat "$output"
        rm -f "$output"
        printf '%s failed without reporting a typing error\n' "$label" >&2
        return 1
    fi
    rm -f "$output"
}

check_negative mypy mypy --strict tests/fixtures/negative.py
check_negative pyright pyright tests/fixtures/negative.py
