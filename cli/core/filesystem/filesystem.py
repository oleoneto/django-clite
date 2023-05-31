# cli:core:filesystem
import os
import io
from typing import IO
from pathlib import Path

from .files import File
from .protocols import SystemProtocol, WriteCommandResult
from cli.core.logger import Logger
from cli.decorators.singleton import singleton


@singleton
class FileSystem:
    def __init__(
        self, debug: bool, dry: bool, force: bool, verbose: bool, system: SystemProtocol
    ):
        self._system = system
        self._debug = debug
        self._dry = dry
        self._force = force
        self._verbose = verbose

    @property
    def dry_mode(cls):
        return cls._dry

    @property
    def system_class(cls):
        return cls._system

    @property
    def force(cls):
        return cls._force

    # -------------------------
    # Core

    def create_file(
        self,
        file: File,
        content: str,
        add_import_statement: bool = False,
        import_statement: str = "",
    ) -> WriteCommandResult:
        created = False
        filepath = Path(file.path)

        # In case the encapsulating folder does not exist, attempt to create it
        # then proceed with the creation of the file
        if not filepath.exists():
            encapsulating_folder = filepath.absolute().parents[0]
            Logger().print(f"Directory {encapsulating_folder} does not exist")
            self.create_directory(encapsulating_folder.__str__())

        try:
            with self._system.open(filepath, mode="w") as f:
                f.write(f"{content}\n")
                Logger().print(f"Wrote contents to {filepath.absolute()}")
                created = True

                # This method needs cleaning up. No clear separation of concerns here.
                if add_import_statement:
                    self.add_line(
                        filepath.parent.absolute() / "__init__.py",
                        import_statement,
                        prevent_duplicates=True,
                    )
        except (FileExistsError, FileNotFoundError) as err:
            print(repr(err))

        return WriteCommandResult(path=filepath.absolute(), success=created)

    def create_directory(self, name: str) -> WriteCommandResult:
        created = False

        try:
            self._system.mkdir(name)
            Logger().print(f"Successfully created directory {name}")
            created = True
        except Exception as err:
            Logger().print(f"Failed to create directory {name}. Error: {repr(err)}")

        return WriteCommandResult(path=Path(name).absolute(), success=created)

    # ----------------------
    # Implements FileHandler

    def add_line(
        self, filename, content, prevent_duplicates: bool = True
    ) -> WriteCommandResult:
        if content is None or content == "":
            return WriteCommandResult(path=Path(), success=False)

        try:
            with self._system.open(filename, mode="r") as file:
                lines = file.readlines() or []

                if prevent_duplicates:
                    for line in lines:
                        # Found a duplicate line. Halt!
                        if line.startswith(content):
                            Logger().print(
                                f"Trying to insert a duplicate statement when duplication control is enabled. Halting!"
                            )
                            return WriteCommandResult(path=Path(), success=False)

                file.write(f"{content}\n")
                Logger().print(
                    f"Inserted import statement into {filename} \n      -> {content}"
                )
        except Exception as err:
            Logger().print(
                f"Failed to insert statement into {filename}. Error: {repr(err)}"
            )

        return WriteCommandResult(path=Path(), success=True)

    def pop_line(self, filename, content) -> WriteCommandResult:
        success = False

        try:
            # Find and yank matched line from file
            with self._system.open(filename, mode="r") as file:
                lines = file.readlines()
                for pos, line in enumerate(lines):
                    if line.startswith(content):
                        lines.pop(pos)
                        Logger().print(f"Removed line at {pos} from {filename}")
                        break

            # Update the contents of the file
            with self._system.open(filename, mode="w") as file:
                file.writelines(lines)
                Logger().print(f"Successfully updated the contents of {filename}")

            success = True
        except Exception as err:
            print(repr(err))

        return WriteCommandResult(path=Path(), success=success)
