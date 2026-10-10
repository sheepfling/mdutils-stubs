class MDListHelper:
    n_tabs: int

    def __init__(self) -> None: ...

class MDList(MDListHelper):
    md_list: str

    def __init__(self, items: list[str], marked_with: str = "-") -> None: ...
    def get_md(self) -> str: ...

class MDCheckbox(MDListHelper):
    checked: str
    md_list: str

    def __init__(self, items: list[str], checked: bool = False) -> None: ...
    def get_md(self) -> str: ...
