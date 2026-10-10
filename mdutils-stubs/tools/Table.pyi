class Table:
    rows: int
    columns: int

    def __init__(self) -> None: ...
    def create_table(
        self,
        columns: int,
        rows: int,
        text: list[str],
        text_align: str | list[str | None] | None = None,
    ) -> str: ...
    def create_table_array(
        self,
        data: list[list[str]],
        text_align: str | list[str | None] | None = None,
    ) -> str: ...
