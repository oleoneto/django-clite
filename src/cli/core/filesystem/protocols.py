# cli:core:filesystem
from pathlib import Path
from typing import Protocol


class FinderProtocol(Protocol):
    def find(self, path: Path, patterns: list[str]) -> dict:
        ...


class FileProtocol(Protocol):
    def create(self, parent: str = None, **kwargs):
        ...

    def path(self, parent: Path = None) -> Path:
        ...
