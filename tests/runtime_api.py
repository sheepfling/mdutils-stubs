from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from tempfile import TemporaryDirectory

import mdutils
from mdutils import MdUtils, TextUtils
from mdutils.fileutils import MarkDownFile
from mdutils.tools.Image import Image as ImageClass
from mdutils.tools.Link import Inline
from mdutils.tools.MDList import MDCheckbox, MDList
from mdutils.tools.TableOfContents import TableOfContents
from mdutils.tools.TextUtils import TextUtils as ModuleTextUtils


def parameter_names(callable_object: object) -> tuple[str, ...]:
    return tuple(inspect.signature(callable_object).parameters)


def main() -> None:
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
    assert MDList(["parent", ["child", ["grandchild"]]]).get_md() == (
        "- parent\n    - child\n        - grandchild\n"
    )
    assert MDCheckbox(["parent", ["child"]]).get_md() == ("- [ ] parent\n    - [ ] child\n")
    helper_list_items = [
        TextUtils.bold("Important"),
        TextUtils.text_color("ready", "green"),
        Inline.new_link("https://example.com", text="site"),
        ImageClass.new_inline_image("diagram", "diagram.png"),
    ]
    assert helper_list_items == [
        "**Important**",
        '<font color="green">ready</font>',
        "[site](https://example.com)",
        "![diagram](diagram.png)",
    ]
    expected_helper_list = (
        "- **Important**\n"
        '- <font color="green">ready</font>\n'
        "- [site](https://example.com)\n"
        "- ![diagram](diagram.png)\n"
    )
    assert MDList(helper_list_items).get_md() == expected_helper_list
    assert MDCheckbox(helper_list_items, checked=True).get_md() == (
        "- [x] **Important**\n"
        '- [x] <font color="green">ready</font>\n'
        "- [x] [site](https://example.com)\n"
        "- [x] ![diagram](diagram.png)\n"
    )
    list_doc = MdUtils("helpers")
    assert (
        list_doc.new_list([helper_list_items[0], [helper_list_items[2], helper_list_items[3]]])
        is None
    )
    assert list_doc.file_data_text == (
        "\n- **Important**\n    - [site](https://example.com)\n    - ![diagram](diagram.png)\n"
    )
    assert TableOfContents().create_table_of_contents(["Parent", ["Child"]], depth=2) == (
        "\n* [Parent](#parent)\n\t* [Child](#child)\n"
    )
    nested_doc = MdUtils("nested")
    assert nested_doc.new_list(["parent", ["child"]]) is None
    assert nested_doc.file_data_text == "\n- parent\n    - child\n"
    assert nested_doc.new_checkbox_list(["parent", ["child"]], checked=True) is None
    assert nested_doc.file_data_text.endswith("\n- [x] parent\n    - [x] child\n")

    with TemporaryDirectory(prefix="mdutils-stubs-runtime-") as temporary_directory:
        path = Path(temporary_directory) / "sample.md"
        markdown_file = MarkDownFile(str(path))
        markdown_file.rewrite_all_file("first\nsecond\nthird")
        contents = MarkDownFile.read_file(str(path))
        assert contents == "first\nsecond\nthird"
        markdown_file.append_after_second_line("inserted")
        contents = MarkDownFile.read_file(str(path))
        assert contents == "first\nsecond\ninserted\nthird"
        markdown_file.append_end("\nlast")
        contents = MarkDownFile.read_file(str(path))
        assert contents == "first\nsecond\ninserted\nthird\nlast"

    assert doc.reference.get_references_as_markdown() == "\n\n\n[site]: https://example.com\n"
    assert (
        str(
            importlib.import_module("mdutils.tools.Header").Header(
                1, "Title", importlib.import_module("mdutils.tools.Header").HeaderStyle.ATX
            )
        )
        == "\n# Title\n"
    )


if __name__ == "__main__":
    main()
