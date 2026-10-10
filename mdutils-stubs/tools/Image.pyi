from .Link import Reference

class Image:
    reference: Reference

    def __init__(self, reference: Reference) -> None: ...
    @staticmethod
    def new_inline_image(text: str, path: str, tooltip: str | None = None) -> str: ...
    def new_reference_image(
        self,
        text: str,
        path: str,
        reference_tag: str | None = None,
        tooltip: str | None = None,
    ) -> str: ...
