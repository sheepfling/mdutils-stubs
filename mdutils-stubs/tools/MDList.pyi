from collections.abc import Sequence as _Sequence
from typing import TypeAlias

_ListItem: TypeAlias = str | _Sequence["_ListItem"]

class MDListHelper:
    n_tabs: int

    def __init__(self) -> None: ...

class MDList(MDListHelper):
    md_list: str

    def __init__(self, items: _Sequence[_ListItem], marked_with: str = "-") -> None: ...
    def get_md(self) -> str: ...

class MDCheckbox(MDListHelper):
    checked: str
    md_list: str

    def __init__(self, items: _Sequence[_ListItem], checked: bool = False) -> None: ...
    def get_md(self) -> str: ...
