from typing import NamedTuple


class Template(NamedTuple):
    filename: str
    template: str
    raw: bool = False
