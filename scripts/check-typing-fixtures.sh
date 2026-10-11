#!/usr/bin/env bash
set -euo pipefail

positive_cache="$(mktemp -d)"
trap 'rm -rf "$positive_cache"' EXIT
mypy --strict --cache-dir "$positive_cache" tests/fixtures/positive.py
pyright --pythonpath "$(command -v python)" tests/fixtures/positive.py

check_negative() {
    local label="$1"
    local expected_count="$2"
    shift 2
    local output
    local cache
    local -a expected_diagnostics
    output="$(mktemp)"
    cache="$(mktemp -d)"
    if [[ "$label" == "mypy" ]]; then
        set -- "$1" --cache-dir "$cache" "${@:2}"
        expected_diagnostics=(
            'Argument "file_name"'
            'Argument "level"'
            'Argument "title"'
            'List item 0'
            'Argument "text_align"'
            'list[_ListItem]'
            'Argument "text"'
        )
    else
        expected_diagnostics=(
            'parameter "file_name"'
            'parameter "level"'
            'parameter "title"'
            'parameter "text" of type "list[str]"'
            'parameter "text_align"'
            'parameter "items" of type "list[_ListItem]"'
            'parameter "text" of type "str"'
        )
    fi
    if "$@" >"$output" 2>&1; then
        cat "$output"
        rm -f "$output"
        rm -rf "$cache"
        printf '%s unexpectedly accepted the negative fixture\n' "$label" >&2
        return 1
    fi
    if [[ "$(rg -c 'error:' "$output" || true)" != "$expected_count" ]]; then
        cat "$output"
        rm -f "$output"
        rm -rf "$cache"
        printf '%s did not report exactly %s expected type errors\n' "$label" "$expected_count" >&2
        return 1
    fi
    for diagnostic in "${expected_diagnostics[@]}"; do
        if ! rg -Fq "$diagnostic" "$output"; then
            cat "$output"
            rm -f "$output"
            rm -rf "$cache"
            printf '%s is missing the expected diagnostic for %s\n' "$label" "$diagnostic" >&2
            return 1
        fi
    done
    rm -f "$output"
    rm -rf "$cache"
}

check_negative mypy 7 mypy --strict tests/fixtures/negative.py
check_negative pyright 7 pyright --pythonpath "$(command -v python)" tests/fixtures/negative.py
