from typing import TypeAlias

_ListItem: TypeAlias = str | list["_ListItem"]

class MDListHelper:
    n_tabs: int

    def __init__(self) -> None: ...

class MDList(MDListHelper):
    md_list: str

    def __init__(self, items: list[_ListItem], marked_with: str = "-") -> None: ...
    def get_md(self) -> str: ...

class MDCheckbox(MDListHelper):
    checked: str
    md_list: str

    def __init__(self, items: list[_ListItem], checked: bool = False) -> None: ...
    def get_md(self) -> str: ...
