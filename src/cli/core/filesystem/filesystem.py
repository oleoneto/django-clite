# cli:core:filesystem
import os
from pathlib import Path
from contextlib import contextmanager

from .protocols import SystemProtocol, WriteCommandResult
from cli.decorators.singleton import singleton
from cli.core.logger import logger


@contextmanager
def working_directory(directory):
    # Based on: https://stackoverflow.com/a/53993508/7899348

    cwd = os.getcwd()

    try:
        os.chdir(directory)
        yield directory
    except FileNotFoundError as _:
        yield
    except TypeError as _:
        yield
    finally:
        os.chdir(cwd)


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
    def dry_mode(self):
        return self._dry

    @property
    def system_class(self):
        return self._system

    @property
    def force(self):
        return self._force

    # ----------------------
    # Implements FileHandler

    def add_line(
        self, filename, content, prevent_duplicates: bool = True
    ) -> WriteCommandResult:
        if content is None or content == "":
            return WriteCommandResult(path=Path(), success=False)

        try:
            with self._system.open(filename, mode="r+") as file:
                lines = file.readlines() or []

                if prevent_duplicates:
                    for line in lines:
                        # Found a duplicate line. Halt!
                        if line.startswith(content):
                            logger.debug(
                                f"Trying to insert a duplicate statement when duplication control is enabled. Halting!"
                            )
                            return WriteCommandResult(path=Path(), success=False)

                file.write(f"{content}\n")
                logger.debug(
                    f"Inserted import statement into {filename} \n      -> {content}"
                )
        except Exception as err:
            logger.debug(
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
                        logger.debug(f"Removed line at {pos} from {filename}")
                        break

            # Update the contents of the file
            with self._system.open(filename, mode="w") as file:
                file.writelines(lines)
                logger.debug(f"Successfully updated the contents of {filename}")

            success = True
        except Exception as err:
            print(repr(err))

        return WriteCommandResult(path=Path(), success=success)
