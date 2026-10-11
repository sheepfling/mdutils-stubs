from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from tempfile import TemporaryDirectory

import mdutils
from mdutils import MdUtils, TextUtils
from mdutils.fileutils import MarkDownFile
from mdutils.tools.TextUtils import TextUtils as ModuleTextUtils


def parameter_names(callable_object: object) -> tuple[str, ...]:
    return tuple(inspect.signature(callable_object).parameters)


assert TextUtils is ModuleTextUtils
assert mdutils.TextUtils is TextUtils
assert mdutils.mdutils is importlib.import_module("mdutils.mdutils")
assert mdutils.tools is importlib.import_module("mdutils.tools")
assert mdutils.fileutils is importlib.import_module("mdutils.fileutils.fileutils")
fileutils_package = importlib.import_module("mdutils.fileutils")
assert fileutils_package.fileutils is mdutils.fileutils
assert fileutils_package.MarkDownFile is MarkDownFile
assert mdutils.tools.TextUtils is TextUtils
assert mdutils.tools.MDList is importlib.import_module("mdutils.tools.MDList").MDList
assert MdUtils("sample").textUtils is TextUtils
assert importlib.import_module("mdutils.tools.TextUtils").TextUtils is TextUtils

assert parameter_names(MdUtils) == (
    "file_name",
    "title",
    "author",
    "title_header_style",
)
assert parameter_names(MdUtils.new_header) == (
    "self",
    "level",
    "title",
    "style",
    "add_table_of_contents",
    "header_id",
)
assert parameter_names(MdUtils.new_table) == (
    "self",
    "columns",
    "rows",
    "text",
    "text_align",
    "marker",
)
assert parameter_names(MdUtils.new_table_array) == (
    "self",
    "data",
    "text_align",
    "marker",
)

doc = MdUtils("sample", title="Example")
assert isinstance(doc.new_table(1, 1, ["head"], text_align=None), str)
marker = doc.create_marker("table-slot")
table_text = doc.new_table_array([["head"], ["value"]], text_align=None, marker=marker)
assert isinstance(table_text, str)
assert marker not in doc.file_data_text
assert table_text in doc.file_data_text

reference_link = doc.new_reference_link("https://example.com", "site", reference_tag=None)
assert reference_link == "[site]"
assert doc.reference.get_references() == {"site": "https://example.com"}
assert (
    doc.new_inline_link("https://example.com", text=None)
    == "[https://example.com](https://example.com)"
)
assert doc.new_list(["one"]) is None
assert doc.new_checkbox_list(["one"]) is None

with TemporaryDirectory(prefix="mdutils-stubs-runtime-") as temporary_directory:
    path = Path(temporary_directory) / "sample.md"
    markdown_file = MarkDownFile(str(path))
    markdown_file.rewrite_all_file("first\nsecond\nthird")
    assert MarkDownFile.read_file(str(path)) == "first\nsecond\nthird"
    markdown_file.append_after_second_line("inserted")
    assert MarkDownFile.read_file(str(path)) == "first\nsecond\ninserted\nthird"
    markdown_file.append_end("\nlast")
    assert MarkDownFile.read_file(str(path)) == "first\nsecond\ninserted\nthird\nlast"

assert doc.reference.get_references_as_markdown() == "\n\n\n[site]: https://example.com\n"
assert (
    str(
        importlib.import_module("mdutils.tools.Header").Header(
            1, "Title", importlib.import_module("mdutils.tools.Header").HeaderStyle.ATX
        )
    )
    == "\n# Title\n"
)
