# cli:core:filesystem
from typing import Protocol
from pathlib import Path


class ReaderProcotol(Protocol):
    def read(self, fd: int, length: int) -> bytes:
        ...

    def open(self, path: Path, flags: int, mode: int = ...) -> int:
        ...

    def close(self, fd: int):
        ...

    def getcwd(self) -> str:
        ...


class WriterProtocol(Protocol):
    def write(self, fd: int, data: bytes) -> int:
        ...

    def remove(self, name: str) -> bool:
        ...

    def create_directory(self, name: str) -> bool:
        ...

    def create_file(self, name: str, content: bytes) -> bool:
        ...


class FileHandlerProtocol(Protocol):
    def pop_line(self, filename: str, content: str) -> bool:
        ...

    def add_line(self, filename: str, content: bytes, prevent_duplicates: bool) -> bool:
        ...


class FinderProtocol(Protocol):
    def find(self, path: Path, patterns: list[str]) -> dict:
        ...
