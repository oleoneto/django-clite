# cli:core
from typing import Protocol


class Git(Protocol):
    def initialize(self) -> bool:
        ...

    def add_origin(self, origin: str) -> bool:
        ...
