# cli:core
import os
from rich.tree import Tree
from typing import Protocol
from pathlib import Path


class Reader(Protocol):
    def read(self, fd: int, length: int) -> bytes:
        ...

    def open(self, path: Path, flags: int, mode: int = ...) -> int:
        ...

    def close(self, fd: int):
        ...

    def getcwd(self) -> str:
        ...

    def find(self, path: Path, patterns: list[str]) -> dict:
        ...


class Writer(Protocol):
    def write(self, fd: int, data: bytes) -> int:
        ...

    def remove(self, name: str) -> bool:
        ...

    def create_directory(self, name: str) -> bool:
        ...

    def create_file(self, name: str, content: bytes) -> bool:
        ...


class FileHandler(Protocol):
    def pop_line(self, filename: str, content: str) -> bool:
        ...

    def add_line(self, filename: str, content: bytes, prevent_duplicates: bool) -> bool:
        ...


class FS(Reader, Writer, FileHandler):
    # --------------------------
    # Implements Reader Protocol

    @classmethod
    def read(cls, fd: int, length: int) -> bytes:
        return os.read(fd, length)

    @classmethod
    def close(cls, fd: int):
        return os.close(fd)

    @classmethod
    def open(cls, path: Path, flags: int, mode: int) -> int:
        return os.open(path, flags, mode)

    @classmethod
    def getcwd(cls) -> str:
        return os.getcwd()

    @classmethod
    def find(cls, path: Path, patterns: list[str]) -> dict:
        files = [fp for fp in path.iterdir() if any(fp.match(p) for p in patterns)]

        matches = dict()
        for match in files:
            matches[match.name] = match.absolute()
        return matches

    # --------------------------
    # Implements Writer Protocol

    @classmethod
    def write(cls, fd, data) -> int:
        return os.write(fd, data)

    @classmethod
    def remove(cls, name: str) -> bool:
        success = False

        try:
            os.remove(name)
            success = True
        except:
            pass

        return success

    @classmethod
    def create_directory(cls, name: str) -> bool:
        success = False

        try:
            os.mkdir(name)
            success = True
        except:
            pass

        return success

    @classmethod
    def create_file(cls, name: str, content: bytes) -> bool:
        success = False

        try:
            with open(name, mode="w") as file:
                file.write(content)
            success = True
        except:
            pass

        return success

    # ----------------------
    # Implements FileHandler

    @classmethod
    def add_line(cls, filename, content, prevent_duplicates: bool = True) -> bool:
        success = False

        try:
            with open(filename, mode="r") as file:
                lines = file.readlines()

                if prevent_duplicates:
                    for index, line in enumerate(lines):
                        if line.startswith(content):
                            return success

                file.write(f"{content}\n")

            success = True
        except:
            pass

        return success

    @classmethod
    def pop_line(cls, filename, content) -> bool:
        success = False

        try:
            # Find and yank matched line from file
            with open(filename, mode="r") as file:
                lines = file.readlines()
                for index, line in enumerate(lines):
                    if line.startswith(content):
                        lines.pop(index)
                        break

            # Update the contents of the file
            with open(filename, mode="w") as file:
                file.writelines(lines)

            success = True
        except:
            pass

        return success


class File:
    def __init__(self, name: str, content: bytes):
        self._name = name
        self._content = content

    @property
    def name(self) -> str:
        return self._name

    @property
    def content(self) -> bytes:
        return self._content


class Directory:
    def __init__(self, name, children=list, files=list[File]):
        self.name = name
        self._children = children
        self._files = files

    def traverse(self, hide_files: bool = False, **kwargs):
        tree = Tree(self.name)

        if not hide_files:
            for file in self.files:
                tree.add(file.filename)

        for child in self.children:
            child_tree = child.traverse(**kwargs)
            tree.add(child_tree)

        return tree

    def add_children(self, children: list, **kwargs):
        for child in children:
            if not type(child) == type(self):
                child = Directory(name=child)
            self._children.append(child)

    def add_files(self, files: list[File], **kwargs):
        for file in files:
            self._files.append(file)

    @property
    def children(self) -> list:
        return self._children

    @property
    def files(self) -> list[File]:
        return self._files
