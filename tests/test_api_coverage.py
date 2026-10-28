"""Structural inventory checks against the installed mdutils runtime source.

These checks compare names and call signatures. They intentionally do not claim
to infer whether each declared type captures the runtime's full semantics; the
external consumer fixtures cover selected positive and negative typing cases.
"""

from __future__ import annotations

import argparse
import importlib
import sys
import unittest
from collections.abc import Sequence
from pathlib import Path
from types import MappingProxyType

from alphus_stub_quality import api_contracts

RUNTIME_MODULES = frozenset(
    {
        "__init__",
        "fileutils/__init__",
        "fileutils/fileutils",
        "mdutils",
        "tools/Header",
        "tools/Html",
        "tools/Image",
        "tools/Link",
        "tools/MDList",
        "tools/Table",
        "tools/TableOfContents",
        "tools/TextUtils",
        "tools/__init__",
    }
)

PACKAGE_EXPORTS = MappingProxyType(
    {
        "mdutils": frozenset(
            {
                "Header",
                "Html",
                "Image",
                "Link",
                "MDList",
                "MdUtils",
                "Table",
                "TableOfContents",
                "TextUtils",
                "fileutils",
                "mdutils",
                "tools",
            }
        ),
        "mdutils.fileutils": frozenset({"MarkDownFile", "fileutils"}),
        "mdutils.tools": frozenset(
            {
                "Header",
                "Html",
                "Image",
                "Inline",
                "Link",
                "MDCheckbox",
                "MDList",
                "SizeBadFormat",
                "Table",
                "TableOfContents",
                "TextUtils",
            }
        ),
    }
)

# The normalized source module and imported name used by each stub package
# initializer. This protects aliases whose runtime package attribute shadows
# the package object with a nested module of the same name.
PACKAGE_STUB_IMPORTS = MappingProxyType(
    {
        "mdutils": MappingProxyType(
            {
                "Header": ("mdutils.tools", "Header"),
                "Html": ("mdutils.tools", "Html"),
                "Image": ("mdutils.tools", "Image"),
                "Link": ("mdutils.tools", "Link"),
                "MDList": ("mdutils.tools", "MDList"),
                "MdUtils": ("mdutils.mdutils", "MdUtils"),
                "Table": ("mdutils.tools", "Table"),
                "TableOfContents": ("mdutils.tools", "TableOfContents"),
                "TextUtils": ("mdutils.tools", "TextUtils"),
                "fileutils": ("mdutils.fileutils", "fileutils"),
                "mdutils": ("mdutils", "mdutils"),
                "tools": ("mdutils", "tools"),
            }
        ),
        "mdutils.fileutils": MappingProxyType(
            {
                "MarkDownFile": ("mdutils.fileutils.fileutils", "MarkDownFile"),
                "fileutils": ("mdutils.fileutils", "fileutils"),
            }
        ),
        "mdutils.tools": MappingProxyType(
            {
                "Header": ("mdutils.tools", "Header"),
                "Html": ("mdutils.tools.Html", "Html"),
                "Image": ("mdutils.tools", "Image"),
                "Inline": ("mdutils.tools.Link", "Inline"),
                "Link": ("mdutils.tools", "Link"),
                "MDCheckbox": ("mdutils.tools.MDList", "MDCheckbox"),
                "MDList": ("mdutils.tools.MDList", "MDList"),
                "SizeBadFormat": ("mdutils.tools.Html", "SizeBadFormat"),
                "Table": ("mdutils.tools", "Table"),
                "TableOfContents": ("mdutils.tools", "TableOfContents"),
                "TextUtils": ("mdutils.tools.TextUtils", "TextUtils"),
            }
        ),
    }
)

EXPORT_TARGETS = MappingProxyType(
    {
        "mdutils": MappingProxyType(
            {
                "Header": ("mdutils.tools.Header", None),
                "Html": ("mdutils.tools.Html", "Html"),
                "Image": ("mdutils.tools.Image", None),
                "Link": ("mdutils.tools.Link", None),
                "MDList": ("mdutils.tools.MDList", "MDList"),
                "MdUtils": ("mdutils.mdutils", "MdUtils"),
                "Table": ("mdutils.tools.Table", None),
                "TableOfContents": ("mdutils.tools.TableOfContents", None),
                "TextUtils": ("mdutils.tools.TextUtils", "TextUtils"),
                "fileutils": ("mdutils.fileutils.fileutils", None),
                "mdutils": ("mdutils.mdutils", None),
                "tools": ("mdutils.tools", None),
            }
        ),
        "mdutils.fileutils": MappingProxyType(
            {
                "MarkDownFile": ("mdutils.fileutils.fileutils", "MarkDownFile"),
                "fileutils": ("mdutils.fileutils.fileutils", None),
            }
        ),
        "mdutils.tools": MappingProxyType(
            {
                "Header": ("mdutils.tools.Header", None),
                "Html": ("mdutils.tools.Html", "Html"),
                "Image": ("mdutils.tools.Image", None),
                "Inline": ("mdutils.tools.Link", "Inline"),
                "Link": ("mdutils.tools.Link", None),
                "MDCheckbox": ("mdutils.tools.MDList", "MDCheckbox"),
                "MDList": ("mdutils.tools.MDList", "MDList"),
                "SizeBadFormat": ("mdutils.tools.Html", "SizeBadFormat"),
                "Table": ("mdutils.tools.Table", None),
                "TableOfContents": ("mdutils.tools.TableOfContents", None),
                "TextUtils": ("mdutils.tools.TextUtils", "TextUtils"),
            }
        ),
    }
)


class PublicApiCoverageTests(api_contracts.ApiCoverageTests):
    __test__ = True
    package_name = "mdutils"
    required_version = "1.8.1"
    module_paths = {
        "mdutils"
        if relative == "__init__"
        else "mdutils." + relative.replace("/", ".").removesuffix(".__init__"): relative
        for relative in RUNTIME_MODULES
    }
    runtime_packages = {
        name: importlib.import_module(name)
        for name in set(PACKAGE_EXPORTS)
        | {
            target_module
            for exports in EXPORT_TARGETS.values()
            for target_module, _ in exports.values()
        }
    }
    package_exports = PACKAGE_EXPORTS
    stub_imports = PACKAGE_STUB_IMPORTS
    export_targets = EXPORT_TARGETS
    fixture_path = Path(__file__).parent / "fixtures" / "positive.py"


def _unittest_arguments(argv: Sequence[str]) -> list[str]:
    """Require the caller to provide the stub fixture path explicitly."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stub-root",
        type=Path,
        required=True,
        help="path to the mdutils-stubs source directory",
    )
    options, remaining = parser.parse_known_args(argv[1:])
    stub_root = options.stub_root.expanduser().resolve()
    if not stub_root.is_dir():
        parser.error(f"stub root is not a directory: {stub_root}")
    PublicApiCoverageTests.stub_root = stub_root
    return [argv[0], *remaining]


if __name__ == "__main__":
    unittest.main(argv=_unittest_arguments(sys.argv))
