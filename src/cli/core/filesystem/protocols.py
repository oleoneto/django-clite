# cli:core:filesystem
import io
from pathlib import Path
from typing import Protocol, NamedTuple


class WriteCommandResult(NamedTuple):
    path: Path
    success: bool = False


class ReadCommandResult(NamedTuple):
    path: Path
    success: bool = False


class ReaderProtocol(Protocol):
    def open(self, path: Path, mode: str = ...) -> io.TextIOWrapper:
        ...

    def close(self, fd: int):
        ...

    def getcwd(self) -> str:
        ...


class WriterProtocol(Protocol):
    def write(self, fd: int, data: bytes) -> int:
        ...

    def remove(self, name: str) -> None:
        ...

    def mkdir(self, name: str) -> None:
        ...


class FileHandlerProtocol(Protocol):
    def pop_line(self, filename: str, content: str) -> bool:
        ...

    def add_line(self, filename: str, content: bytes, prevent_duplicates: bool) -> bool:
        ...


class FinderProtocol(Protocol):
    def find(self, path: Path, patterns: list[str]) -> dict:
        ...


class SystemProtocol(ReaderProtocol, WriterProtocol, Protocol):
    ...


class FileProtocol(Protocol):
    def create(self, parent: str = None, **kwargs):
        ...

    def path(self, parent: Path = None) -> Path:
        ...
