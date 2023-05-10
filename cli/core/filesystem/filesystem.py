# cli:core:filesystem
import os
from pathlib import Path
from .protocols import (
    ReaderProcotol,
    WriterProtocol,
    FileHandlerProtocol,
    FinderProtocol,
)
from .files import File
from cli.decorators import singleton
from typing import Union


class Finder(FinderProtocol):
    @classmethod
    def find(cls, path: Path, patterns: list[str]) -> dict:
        files = [fp for fp in path.iterdir() if any(fp.match(p) for p in patterns)]

        matches = dict()
        for match in files:
            matches[match.name] = match.absolute()
        return matches


class NullOS:
    @classmethod
    def read(cls, *args, **kwargs):
        return None

    @classmethod
    def close(cls, *args, **kwargs):
        return None

    @classmethod
    def open(cls, *args, **kwargs):
        return None

    @classmethod
    def getcwd(cls):
        return None

    @classmethod
    def mkdir(cls, *args, **kwargs):
        return None

    @classmethod
    def find(cls, *args, **kwargs):
        return None

    @classmethod
    def write(cls, *args, **kwargs):
        return None

    @classmethod
    def remove(cls, *args, **kwargs):
        return None

    @classmethod
    def create_directory(cls, *args, **kwargs):
        return None

    @classmethod
    def create_file(cls, *args, **kwargs):
        return None

    def __repr__(self):
        return "null_os"


@singleton
class FileSystem(ReaderProcotol, WriterProtocol, FileHandlerProtocol):
    _debug: bool = False
    _dry: bool = True
    _force: bool = False
    _verbose: bool = False
    _system = Union[NullOS, os]

    def __init__(self, debug: bool, dry: bool, force: bool, verbose: bool):
        self._debug = debug
        self._dry = dry
        self._force = force
        self._verbose = verbose

        self._system = NullOS() if dry else os

    # Properties

    @property
    def dry_mode(cls):
        return cls._dry

    @property
    def system_class(cls):
        return cls._system

    @property
    def force(cls):
        return cls._force

    @classmethod
    def create_file(cls, file: File, content: bytes):
        print(file.path)
        print(content)

    # --------------------------
    # Implements Reader Protocol

    # @classmethod
    # def read(cls, fd: int, length: int) -> bytes:
    #     return self._system.read(fd, length)

    # @classmethod
    # def close(cls, fd: int):
    #     return self._system.close(fd)

    # @classmethod
    # def open(cls, path: Path, flags: int, mode: int) -> int:
    #     return self._system.open(path, flags, mode)

    # @classmethod
    # def getcwd(cls) -> str:
    #     return self._system.getcwd()

    # # --------------------------
    # # Implements Writer Protocol

    # @classmethod
    # def write(cls, fd, data) -> int:
    #     return self._system.write(fd, data)

    # @classmethod
    # def remove(cls, name: str) -> bool:
    #     success = False

    #     try:
    #         self._system.remove(name)
    #         success = True
    #     except Exception as err:
    #         pass

    #     return success

    # @classmethod
    # def create_directory(cls, name: str) -> bool:
    #     success = False

    #     try:
    #         cls._system.mkdir(name)
    #         success = True
    #     except Exception as err:
    #         print(repr(err))

    #     return success

    # @classmethod
    # def create_file(cls, name: str, content: bytes) -> bool:
    #     success = False

    #     # TODO: Clean this up
    #     if isinstance(cls._system, NullOS):
    #         cls._system.create_file(name, content)
    #         print("HERE.1")
    #         return True

    #     try:
    #         print("HERE.2")
    #         f = Path(name)
    #         if not f.parent.exists():
    #             cls.create_directory(f.parent)

    #         with open(name, mode="w") as file:
    #             file.write(content)
    #         success = True
    #     except Exception as err:
    #         print(repr(err))

    #     return success

    # # ----------------------
    # # Implements FileHandler

    # @classmethod
    # def add_line(cls, filename, content, prevent_duplicates: bool = True) -> bool:
    #     success = False

    #     # TODO: Clean this up
    #     if isinstance(cls._system, NullOS):
    #         cls._system.add_line(filename, content, prevent_duplicates)
    #         return True

    #     try:
    #         with open(filename, mode="r") as file:
    #             lines = file.readlines()

    #             if prevent_duplicates:
    #                 for index, line in enumerate(lines):
    #                     if line.startswith(content):
    #                         return success

    #             file.write(f"{content}\n")

    #         success = True
    #     except Exception as err:
    #         print(repr(err))

    #     return success

    # @classmethod
    # def pop_line(cls, filename, content) -> bool:
    #     success = False

    #     # TODO: Clean this up
    #     if isinstance(cls._system, NullOS):
    #         cls._system.pop_line(filename, content)
    #         return True

    #     try:
    #         # Find and yank matched line from file
    #         with open(filename, mode="r") as file:
    #             lines = file.readlines()
    #             for index, line in enumerate(lines):
    #                 if line.startswith(content):
    #                     lines.pop(index)
    #                     break

    #         # Update the contents of the file
    #         with open(filename, mode="w") as file:
    #             file.writelines(lines)

    #         success = True
    #     except Exception as err:
    #         print(repr(err))

    #     return success
