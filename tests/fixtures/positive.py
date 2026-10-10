import mdutils
from mdutils import (
    Header,
    Html,
    Image,
    Link,
    MDList,
    MdUtils,
    Table,
    TableOfContents,
    TextUtils,
    fileutils,
)
from mdutils.fileutils import MarkDownFile
from mdutils.fileutils.fileutils import MarkDownFile as FileModuleMarkDownFile
from mdutils.mdutils import MdUtils as ModuleMdUtils
from mdutils.tools import TextUtils as ToolsTextUtils
from mdutils.tools.Header import (
    AtxHeaderLevel,
    HeaderStyle,
    SetextHeaderLevel,
)
from mdutils.tools.Header import (
    Header as HeaderClass,
)
from mdutils.tools.Html import HtmlSize, SizeBadFormat
from mdutils.tools.Image import Image as ImageClass
from mdutils.tools.Link import Inline, Reference
from mdutils.tools.MDList import MDCheckbox, MDListHelper
from mdutils.tools.MDList import MDList as MDListClass
from mdutils.tools.Table import Table as TableClass
from mdutils.tools.TableOfContents import TableOfContents as TOCClass
from mdutils.tools.TextUtils import TextUtils as TextUtilsClass
from typing_extensions import assert_type

document: MdUtils = MdUtils(
    file_name="example", title="Example", author="Rick", title_header_style="atx"
)
assert_type(document, MdUtils)
assert_type(document.textUtils, type[TextUtilsClass])
assert_type(mdutils.TextUtils, type[TextUtilsClass])
assert_type(ToolsTextUtils, type[TextUtilsClass])
assert_type(document.new_header(2, "Section", "atx", "y", "section"), str)
assert_type(document.new_table_of_contents("Contents", depth=2, marker="toc"), str)
assert_type(document.new_table(2, 2, ["A", "B", "1", "2"], text_align=["left", None]), str)
assert_type(document.new_table_array([["A"], ["1"]], text_align=None), str)
assert_type(document.new_paragraph("text", bold_italics_code="b", wrap_width=40), str)
assert_type(document.new_line("text", color="blue", align="center"), str)
assert_type(document.write("marker text", marker="target"), str)
assert_type(document.insert_code("print(1)", language="python"), str)
assert_type(document.create_marker("target"), str)
assert_type(document.place_text_using_marker("replacement", "target"), str)
assert_type(document.new_inline_link("https://example.com", text=None), str)
assert_type(document.new_reference_link("https://example.com", "site", reference_tag=None), str)
assert_type(MdUtils.new_inline_image("alt", "image.png"), str)
assert_type(document.new_reference_image("alt", "image.png", reference_tag=None), str)
assert_type(document.new_list(["one", "two"]), None)
assert_type(document.new_checkbox_list(["one"], checked=True), None)

markdown_file: MarkDownFile = MarkDownFile("example")
assert_type(FileModuleMarkDownFile.read_file("example"), str)
assert_type(markdown_file.append_end("content"), None)
assert_type(document.create_md_file(), MarkDownFile)
assert_type(document.get_md_text(), str)
assert_type(document.read_md_file("example"), str)

header = HeaderClass(1, "Title", HeaderStyle.ATX, "title")
assert_type(header, HeaderClass)
assert_type(HeaderClass.atx(AtxHeaderLevel.TITLE, "Title"), str)
assert_type(HeaderClass.setext(SetextHeaderLevel.HEADING, "Section"), str)
assert_type(HeaderClass.header_anchor("Section", link="custom"), str)
assert_type(HeaderClass.choose_header(1, "Title", style="atx"), str)
assert_type(Html.paragraph("text", align=None), str)
assert_type(Html.image("image.png", size="200x100", align="center"), str)
assert_type(HtmlSize.size_to_width_and_height("200x100"), str)
assert_type(ImageClass.new_inline_image("alt", "image.png", tooltip=None), str)
assert_type(ImageClass(Reference()).new_reference_image("alt", "image.png"), str)
assert_type(Inline.new_link("https://example.com", text=None), str)
assert_type(Reference().new_link("https://example.com", "site"), str)
assert_type(MDListClass(["one"], marked_with="-").get_md(), str)
assert_type(MDCheckbox(["one"], checked=True).get_md(), str)
assert_type(MDListHelper().n_tabs, int)
assert_type(TableClass().create_table(1, 1, ["head"], text_align=None), str)
assert_type(TableClass().create_table_array([["head"], ["row"]]), str)
assert_type(TOCClass().create_table_of_contents(["Heading", ["Nested"]]), str)
assert_type(TextUtilsClass.bold("text"), str)
assert_type(TextUtilsClass.italics("text"), str)
assert_type(TextUtilsClass.inline_code("text"), str)
assert_type(TextUtilsClass.center_text("text"), str)
assert_type(TextUtilsClass.text_color("text", "blue"), str)
assert_type(TextUtilsClass.text_external_link("text", "https://example.com"), str)
assert_type(TextUtilsClass.insert_code("pass", "python"), str)
assert_type(TextUtilsClass.text_format("text", align="center"), str)
assert_type(TextUtilsClass.add_tooltip("https://example.com", "tip"), str)

_exports = (
    Header,
    Html,
    Image,
    Link,
    MDList,
    ModuleMdUtils,
    Table,
    TableOfContents,
    TextUtils,
    fileutils,
    SizeBadFormat,
)
