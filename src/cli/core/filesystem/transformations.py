# cli:core:filesystem:transformations
from typing import Protocol
from pathlib import Path


class FileTransformation(Protocol):
    def run(self):
        ...


class MoveFile(FileTransformation):
    def __init__(self, file: str, target: str):
        self.file = file
        self.target = target

    def run(self):
        from_ = Path(self.file)
        to_ = Path(self.target)
        from_.rename(to_)


class DeleteFile(FileTransformation):
    def __init__(self, file: str):
        self.file = file

    def run(self):
        file = Path(self.file)
        file.unlink(missing_ok=True)


class AddLineToFile(FileTransformation):
    def __init__(self, target: Path, statement: str, prevent_duplicates: bool = True):
        self.target = target
        self.statement = statement
        self.prevent_duplicates = prevent_duplicates

    def run(self):
        if self.statement is None or self.statement == "":
            return

        try:
            with open(self.target, mode="r+") as f:
                lines = f.readlines() or []

                if self.prevent_duplicates:
                    for line in lines:
                        # Found a duplicate line. Halt!
                        if line.startswith(self.statement):
                            return

                f.write(f"{self.statement}\n")
        except (FileNotFoundError, OSError) as _:
            pass


class RemoveLineFromFile(FileTransformation):
    def __init__(self, target: Path, statement: str):
        self.target = target
        self.statement = statement

    def run(self):
        if self.statement is None or self.statement == "":
            return

        try:
            # Find and yank matched line from file
            with open(self.target, mode='r') as f:
                lines = f.readlines()
                for pos, line in enumerate(lines):
                    if line.startswith(self.statement):
                        lines.pop(pos)
                        break

            with open(self.target, mode='w') as f:
                f.writelines(lines)
        except (FileNotFoundError, OSError) as _:
            pass
