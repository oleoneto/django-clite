# cli:core:filesystem
import os
from pathlib import Path
from .protocols import Reader, Writer, FileHandler


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


class NullFS(Reader, Writer, FileHandler):
    # --------------------------
    # Implements Reader Protocol

    @classmethod
    def read(cls, fd: int, length: int) -> bytes:
        return b""

    @classmethod
    def close(cls, fd: int):
        return None

    @classmethod
    def open(cls, path: Path, flags: int, mode: int) -> int:
        return -1

    @classmethod
    def getcwd(cls) -> str:
        return os.getcwd()

    @classmethod
    def find(cls, path: Path, patterns: list[str]) -> dict:
        matches = dict()
        return matches

    # --------------------------
    # Implements Writer Protocol

    @classmethod
    def write(cls, fd, data) -> int:
        return -1

    @classmethod
    def remove(cls, name: str) -> bool:
        return True

    @classmethod
    def create_directory(cls, name: str) -> bool:
        return True

    @classmethod
    def create_file(cls, name: str, content: bytes) -> bool:
        return True

    # ----------------------
    # Implements FileHandler

    @classmethod
    def add_line(cls, filename, content, prevent_duplicates: bool = True) -> bool:
        return True

    @classmethod
    def pop_line(cls, filename, content) -> bool:
        return True
