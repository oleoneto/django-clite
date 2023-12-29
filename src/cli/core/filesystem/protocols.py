# cli:core:filesystem
import io
from pathlib import Path
from typing import Protocol, NamedTuple


class FinderProtocol(Protocol):
    def find(self, path: Path, patterns: list[str]) -> dict:
        ...


class FileProtocol(Protocol):
    def create(self, parent: str = None, **kwargs):
        ...

    def path(self, parent: Path = None) -> Path:
        ...
