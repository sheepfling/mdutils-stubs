from typing import TypeAlias

_TocEntry: TypeAlias = str | list["_TocEntry"]

class TableOfContents:
    def create_table_of_contents(
        self, array_of_title_contents: list[_TocEntry], depth: int = 1
    ) -> str: ...
