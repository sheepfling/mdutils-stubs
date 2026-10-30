from typing import TextIO, TypeAlias

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
from mdutils import (
    mdutils as RootMdUtilsModule,
)
from mdutils import (
    tools as RootToolsModule,
)
from mdutils.fileutils import MarkDownFile
from mdutils.fileutils import fileutils as FileUtilsModule
from mdutils.fileutils.fileutils import MarkDownFile as FileModuleMarkDownFile
from mdutils.mdutils import MdUtils as ModuleMdUtils
from mdutils.tools import (
    Header as ToolsHeaderModule,
)
from mdutils.tools import (
    Html as ToolsHtml,
)
from mdutils.tools import (
    Image as ToolsImageModule,
)
from mdutils.tools import (
    Inline,
    MDCheckbox,
    SizeBadFormat,
)
from mdutils.tools import (
    Link as ToolsLinkModule,
)
from mdutils.tools import (
    MDList as ToolsMDList,
)
from mdutils.tools import (
    Table as ToolsTableModule,
)
from mdutils.tools import (
    TableOfContents as ToolsTableOfContentsModule,
)
from mdutils.tools import (
    TextUtils as ToolsTextUtils,
)
from mdutils.tools.Header import (
    AtxHeaderLevel,
    HeaderStyle,
    SetextHeaderLevel,
)
from mdutils.tools.Header import (
    Header as HeaderClass,
)
from mdutils.tools.Html import Html as HtmlClass
from mdutils.tools.Html import HtmlSize
from mdutils.tools.Image import Image as ImageClass
from mdutils.tools.Link import Reference
from mdutils.tools.MDList import MDList as MDListClass
from mdutils.tools.MDList import MDListHelper
from mdutils.tools.Table import Table as TableClass
from mdutils.tools.TableOfContents import TableOfContents as TOCClass
from mdutils.tools.TextUtils import TextUtils as TextUtilsClass
from typing_extensions import assert_type

document: MdUtils = MdUtils(
    file_name="example", title="Example", author="Rick", title_header_style="atx"
)

_ListItem: TypeAlias = str | list["_ListItem"]
assert_type(document, MdUtils)
_mdutils_class: type[MdUtils] = MdUtils
_mdlist_class: type[MDList] = MDList
_text_utils_class: type[TextUtils] = TextUtils
_header_class: type[HeaderClass] = Header.Header
_image_class: type[ImageClass] = Image.Image
_inline_class: type[Inline] = Link.Inline
_reference_class: type[Reference] = Link.Reference
_table_class: type[TableClass] = Table.Table
_toc_class: type[TOCClass] = TableOfContents.TableOfContents
_mark_down_file_class: type[MarkDownFile] = fileutils.MarkDownFile
_root_mdutils_class: type[MdUtils] = RootMdUtilsModule.MdUtils
_root_text_utils_class: type[TextUtilsClass] = RootToolsModule.TextUtils
_file_module_class: type[MarkDownFile] = FileUtilsModule.MarkDownFile
_tools_header_class: type[HeaderClass] = ToolsHeaderModule.Header
_tools_image_class: type[ImageClass] = ToolsImageModule.Image
_tools_inline_class: type[Inline] = ToolsLinkModule.Inline
_tools_reference_class: type[Reference] = ToolsLinkModule.Reference
_tools_table_class: type[TableClass] = ToolsTableModule.Table
_tools_toc_class: type[TOCClass] = ToolsTableOfContentsModule.TableOfContents
_html_class: type[Html] = Html
_html_module_class: type[HtmlClass] = HtmlClass
_tools_html_class: type[ToolsHtml] = ToolsHtml
_tools_mdlist_class: type[ToolsMDList] = ToolsMDList
_link_class: type[Inline] = Inline
_checkbox_class: type[MDCheckbox] = MDCheckbox
_size_error_class: type[SizeBadFormat] = SizeBadFormat
_tools_text_utils_class: type[ToolsTextUtils] = ToolsTextUtils
_instance_text_utils_class: type[TextUtilsClass] = document.textUtils
_root_text_utils_alias: type[TextUtilsClass] = mdutils.TextUtils
_tools_text_utils_alias: type[TextUtilsClass] = ToolsTextUtils
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
assert_type(document.new_list(["one", ["nested", ["deeper"]]]), None)
assert_type(document.new_checkbox_list(["one", ["nested"]], checked=True), None)
flat_list_items: list[str] = ["one", "two"]
recursive_list_items: list[_ListItem] = [
    "one",
    ["nested", ["deeper"]],
]
helper_list_items: list[str] = [
    TextUtilsClass.bold("Important"),
    TextUtilsClass.text_external_link("docs", "https://example.com"),
    Inline.new_link("https://example.com", text="site"),
    ImageClass.new_inline_image("diagram", "diagram.png"),
]
assert_type(document.new_list(flat_list_items), None)
assert_type(document.new_list(recursive_list_items), None)
assert_type(document.new_list(helper_list_items), None)
assert_type(document.new_checkbox_list(flat_list_items), None)
assert_type(document.new_checkbox_list(recursive_list_items, checked=True), None)
assert_type(document.new_checkbox_list(helper_list_items, checked=True), None)
assert_type(document.file_name, str)
assert_type(document.author, str)
assert_type(document.title, str)
assert_type(document.table_of_contents, str)
assert_type(document.file_data_text, str)
assert_type(document.reference, Reference)
assert_type(document.image, ImageClass)

markdown_file: MarkDownFile = MarkDownFile("example")
assert_type(markdown_file.dirname, str | None)
assert_type(markdown_file.file_name, str)
assert_type(markdown_file.file, TextIO)
assert_type(FileModuleMarkDownFile.read_file("example"), str)
assert_type(markdown_file.append_end("content"), None)
assert_type(markdown_file.rewrite_all_file("replacement"), None)
assert_type(markdown_file.append_after_second_line("inserted"), None)
assert_type(document.create_md_file(), MarkDownFile)
assert_type(document.get_md_text(), str)
assert_type(document.read_md_file("example"), str)

header = HeaderClass(1, "Title", HeaderStyle.ATX, "title")
assert_type(header, HeaderClass)
assert_type(header.level, int)
assert_type(header.title, str)
assert_type(header.style, HeaderStyle)
assert_type(header.header_id, str | None)
assert_type(str(header), str)
_enum_members = (
    AtxHeaderLevel.TITLE,
    AtxHeaderLevel.HEADING,
    AtxHeaderLevel.SUBHEADING,
    AtxHeaderLevel.SUBSUBHEADING,
    AtxHeaderLevel.MINORHEADING,
    AtxHeaderLevel.LEASTHEADING,
    SetextHeaderLevel.TITLE,
    SetextHeaderLevel.HEADING,
    HeaderStyle.ATX,
    HeaderStyle.SETEXT,
)
assert_type(SizeBadFormat("invalid size"), SizeBadFormat)
assert_type(HeaderClass.atx(AtxHeaderLevel.TITLE, "Title"), str)
assert_type(HeaderClass.setext(SetextHeaderLevel.HEADING, "Section"), str)
assert_type(HeaderClass.header_anchor("Section", link="custom"), str)
assert_type(HeaderClass.choose_header(1, "Title", style="atx"), str)
assert_type(Html.paragraph("text", align=None), str)
assert_type(Html.image("image.png", size="200x100", align="center"), str)
assert_type(HtmlSize.size_to_width_and_height("200x100"), str)
assert_type(ImageClass.new_inline_image("alt", "image.png", tooltip=None), str)
assert_type(ImageClass(Reference()).new_reference_image("alt", "image.png"), str)
assert_type(ImageClass(Reference()).reference, Reference)
assert_type(Inline.new_link("https://example.com", text=None), str)
assert_type(Reference().new_link("https://example.com", "site"), str)
assert_type(Reference().references, dict[str, str])
assert_type(Reference().get_references(), dict[str, str])
assert_type(Reference().get_references_as_markdown(), str)
assert_type(MDListClass(["one", ["nested", ["deeper"]]], marked_with="-").get_md(), str)
assert_type(MDListClass(flat_list_items).get_md(), str)
assert_type(MDListClass(recursive_list_items).get_md(), str)
assert_type(MDListClass(helper_list_items).get_md(), str)
assert_type(MDCheckbox(flat_list_items).get_md(), str)
assert_type(MDCheckbox(recursive_list_items, checked=True).get_md(), str)
assert_type(MDCheckbox(helper_list_items, checked=True).get_md(), str)
assert_type(
    MDListClass(
        [
            TextUtilsClass.bold("Important"),
            [
                TextUtilsClass.text_external_link("docs", "https://example.com"),
                Inline.new_link("https://example.com", text="site"),
                ImageClass.new_inline_image("diagram", "diagram.png"),
            ],
        ]
    ).get_md(),
    str,
)
assert_type(
    MDCheckbox(
        [
            TextUtilsClass.bold("Important"),
            [
                TextUtilsClass.text_external_link("docs", "https://example.com"),
                Inline.new_link("https://example.com", text="site"),
                ImageClass.new_inline_image("diagram", "diagram.png"),
            ],
        ],
        checked=True,
    ).get_md(),
    str,
)
assert_type(
    document.new_list(
        [
            TextUtilsClass.bold("Important"),
            [
                TextUtilsClass.text_external_link("docs", "https://example.com"),
                Inline.new_link("https://example.com", text="site"),
                ImageClass.new_inline_image("diagram", "diagram.png"),
            ],
        ]
    ),
    None,
)
assert_type(
    document.new_checkbox_list(
        [
            TextUtilsClass.bold("Important"),
            [
                TextUtilsClass.text_external_link("docs", "https://example.com"),
                Inline.new_link("https://example.com", text="site"),
                ImageClass.new_inline_image("diagram", "diagram.png"),
            ],
        ],
        checked=True,
    ),
    None,
)
assert_type(MDListClass(["one"]).md_list, str)
assert_type(MDCheckbox(["one", ["nested"]], checked=True).get_md(), str)
assert_type(MDCheckbox(["one"], checked=True).checked, str)
assert_type(MDCheckbox(["one"]).md_list, str)
assert_type(MDListHelper().n_tabs, int)
assert_type(TableClass().create_table(1, 1, ["head"], text_align=None), str)
assert_type(TableClass().create_table_array([["head"], ["row"]]), str)
assert_type(TableClass().rows, int)
assert_type(TableClass().columns, int)
assert_type(TOCClass().create_table_of_contents(["Heading", ["Nested"]], depth=2), str)
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
