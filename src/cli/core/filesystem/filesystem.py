# cli:core:filesystem
from pathlib import Path
from .protocols import SystemProtocol, WriteCommandResult
from cli.decorators.singleton import singleton
from cli.core.logger import logger


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

    # -------------------------
    # Core

    def create(self, name: str, is_dir: bool):
        path = Path(name)

        logger.info(f"create: {path}")

        if self.dry_mode:
            return

        if is_dir:
            path.mkdir(exist_ok=True)
            return

        path.touch(exist_ok=True)

    def create_file(
        self,
        file,
        content: str,
        add_import_statement: bool = False,
        import_statement: str = "",
    ) -> WriteCommandResult:
        created = False
        filepath = Path(file.path())

        # In case the encapsulating folder does not exist, attempt to create it
        # then proceed with the creation of the file
        if not filepath.exists():
            encapsulating_folder = filepath.absolute().parents[0]
            logger.debug(f"Directory {encapsulating_folder.name} does not exist")
            self.create_directory(encapsulating_folder)

        try:
            with self._system.open(filepath, mode="w") as f:
                f.write(f"{content}\n")
                logger.debug(f"Wrote contents to {filepath.absolute()}")
                created = True

                # This method needs cleaning up. No clear separation of concerns here.
                if add_import_statement:
                    self.add_line(
                        filepath.parent.absolute() / "__init__.py",
                        import_statement,
                        prevent_duplicates=True,
                    )

            logger.info(f"created {filepath}")
        except (FileExistsError, FileNotFoundError) as err:
            print(repr(err))

        return WriteCommandResult(path=filepath.absolute(), success=created)

    def create_directory(self, path: Path) -> WriteCommandResult:
        created = False

        try:
            self._system.mkdir(path.__str__())
            created = True
            logger.debug(f"Successfully created directory {path.name}")
            logger.info(f"created {path.name}")
        except Exception as err:
            logger.debug(f"Failed to create directory {path.name}. Error: {repr(err)}")

        return WriteCommandResult(path=path.absolute(), success=created)

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
