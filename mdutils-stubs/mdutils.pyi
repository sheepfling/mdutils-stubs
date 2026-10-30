"""Public facade and builder class for mdutils."""

from collections.abc import Sequence as _Sequence
from textwrap import fill as fill
from typing import TypeAlias

from .fileutils.fileutils import MarkDownFile as MarkDownFile
from .tools import Table as Table
from .tools import TableOfContents as TableOfContents
from .tools.Header import Header as Header
from .tools.Header import HeaderStyle as HeaderStyle
from .tools.Image import Image as Image
from .tools.Link import Inline as Inline
from .tools.Link import Reference as Reference
from .tools.MDList import MDCheckbox as MDCheckbox
from .tools.MDList import MDList as MDList
from .tools.TextUtils import TextUtils as TextUtils

_ListItem: TypeAlias = str | list["_ListItem"]

class MdUtils:
    file_name: str
    author: str
    textUtils: type[TextUtils]
    title: str
    table_of_contents: str
    file_data_text: str
    reference: Reference
    image: Image

    def __init__(
        self,
        file_name: str,
        title: str = "",
        author: str = "",
        title_header_style: str = "setext",
    ) -> None: ...
    def create_md_file(self) -> MarkDownFile: ...
    def get_md_text(self) -> str: ...
    def read_md_file(self, file_name: str) -> str: ...
    def new_header(
        self,
        level: int,
        title: str,
        style: str = "atx",
        add_table_of_contents: str = "y",
        header_id: str = "",
    ) -> str: ...
    def new_table_of_contents(
        self, table_title: str = "Table of contents", depth: int = 1, marker: str = ""
    ) -> str: ...
    def new_table(
        self,
        columns: int,
        rows: int,
        text: list[str],
        text_align: str | list[str | None] | None = "center",
        marker: str = "",
    ) -> str: ...
    def new_table_array(
        self,
        data: list[list[str]],
        text_align: str | list[str | None] | None = None,
        marker: str = "",
    ) -> str: ...
    def new_paragraph(
        self,
        text: str = "",
        bold_italics_code: str = "",
        color: str = "black",
        align: str = "",
        wrap_width: int = 0,
    ) -> str: ...
    def new_line(
        self,
        text: str = "",
        bold_italics_code: str = "",
        color: str = "black",
        align: str = "",
        wrap_width: int = 0,
    ) -> str: ...
    def write(
        self,
        text: str = "",
        bold_italics_code: str = "",
        color: str = "black",
        align: str = "",
        marker: str = "",
        wrap_width: int = 0,
    ) -> str: ...
    def insert_code(self, code: str, language: str = "") -> str: ...
    def create_marker(self, text_marker: str) -> str: ...
    def place_text_using_marker(self, text: str, marker: str) -> str: ...
    def new_inline_link(
        self,
        link: str,
        text: str | None = None,
        bold_italics_code: str = "",
        align: str = "",
    ) -> str: ...
    def new_reference_link(
        self,
        link: str,
        text: str,
        reference_tag: str | None = None,
        bold_italics_code: str = "",
        align: str = "",
    ) -> str: ...
    @staticmethod
    def new_inline_image(text: str, path: str) -> str: ...
    def new_reference_image(
        self, text: str, path: str, reference_tag: str | None = None
    ) -> str: ...
    def new_list(self, items: _Sequence[_ListItem], marked_with: str = "-") -> None: ...
    def new_checkbox_list(self, items: _Sequence[_ListItem], checked: bool = False) -> None: ...
