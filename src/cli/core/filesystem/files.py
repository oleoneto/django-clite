# cli:core:filesystem
from pathlib import Path
from cli.core.logger import logger
from cli.core.templates.template import TemplateParser
from .filesystem import FileSystem


class File:
    def __init__(self, name: str, template: str = "", content="", context: dict = None):
        self.context = context if context is not None else {}
        self._name = name
        self._template = template
        self._content = content

    @property
    def name(self) -> str:
        return self._name

    @property
    def template(self) -> str:
        return self._template

    @property
    def contents(self) -> str:
        if self.template != "":
            content = TemplateParser().parse_file(
                filepath=self.template,
                variables=self.context,
            )

            return content

        return self._content

    def path(self, parent: Path = None) -> Path:
        value = Path(self.name) if parent is None else parent / self.name
        return value

    def create(self, parent: Path = None, **kwargs):
        path = self.path(parent)

        logger.info(f"create: {path}")

        # NOTE: Handle missing intermediate directories
        if not path.absolute().parent.exists():
            missing = []  # stack up folders that need to be created

            for p in path.parents:
                if not p.exists():
                    missing.insert(0, p)
                    logger.debug(f"Parent directory {p.name} do not exist")

            [p.mkdir(exist_ok=True) for p in missing if len(missing) != 0]

        path.touch(exist_ok=True)

        if self.contents != "":
            with open(path, mode="w") as f:
                f.write(f"{self.contents}\n")
                logger.debug(f"Add contents to {path.absolute()}")

            # TODO: Add import statement

            should_be_imported = kwargs.get("add_import_statement", False)
            import_statement = kwargs.get("import_statement", "")
            import_location = path.parent.absolute() / "__init__.py"

            if should_be_imported:
                FileSystem().add_line(
                    import_location,
                    import_statement,
                    prevent_duplicates=True,
                )

    def __str__(self) -> str:
        return self.name

    # Implements Sortable

    def __lt__(self, other):
        return self.name < other.name
