class Reference:
    references: dict[str, str]

    def __init__(self) -> None: ...
    def get_references(self) -> dict[str, str]: ...
    def get_references_as_markdown(self) -> str: ...
    def new_link(
        self,
        link: str,
        text: str,
        reference_tag: str | None = None,
        tooltip: str | None = None,
    ) -> str: ...

class Inline:
    @staticmethod
    def new_link(link: str, text: str | None = None, tooltip: str | None = None) -> str: ...
