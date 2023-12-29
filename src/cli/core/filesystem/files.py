# cli:core:filesystem
from pathlib import Path
from cli.core.logger import logger
from .transformations import AddLineToFile, RemoveLineFromFile
from cli.core.templates.template import TemplateParser


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

    def contents(self, **kwargs) -> str:
        if self.template != "":
            self.context.update(**kwargs)

            content = TemplateParser().parse_file(
                filepath=self.template,
                variables=self.context,
            )

            return content

        content = TemplateParser().parse_string(
            self._content,
            variables=self.context
        )

        return content

    def path(self, parent: Path = None) -> Path:
        value = Path(self.name) if parent is None else parent / self.name
        return value

    def create(self, parent: Path = None, **kwargs):
        path = self.path(parent)

        logger.info(f"create: {path}")

        if path.exists():
            logger.error(f"File already exists: {path}")
            return

        # NOTE: Handle missing intermediate directories
        if not path.absolute().parent.exists():
            missing = []  # stack up folders that need to be created

            for p in path.parents:
                if not p.exists():
                    missing.insert(0, p)
                    logger.debug(f"Parent directory {p.name} do not exist")

            [p.mkdir(exist_ok=True) for p in missing if len(missing) != 0]

        path.touch(exist_ok=True)

        contents = self.contents(**kwargs)

        if contents != "":
            path.write_text(f"{contents}\n")

            logger.debug(f"Add contents to {path.absolute()}")

            should_be_imported = kwargs.get("add_import_statement", False)
            import_statement = kwargs.get("import_statement", "")
            import_location = path.parent / "__init__.py"

            # TODO: Add import statement

            if should_be_imported:
                transformation = AddLineToFile(
                    target=import_location,
                    statement=import_statement,
                    prevent_duplicates=True,
                )
                transformation.run()

    def destroy(self, parent: Path = None, **kwargs):
        path = self.path(parent)

        logger.info(f"delete: {path}")

        path.unlink(missing_ok=True)

        # TODO: Yank import statement

        import_statement = kwargs.get("import_statement", "")
        import_location = path.parent / "__init__.py"

        transformation = RemoveLineFromFile(
            target=import_location,
            statement=import_statement,
        )

        transformation.run()

    def __str__(self) -> str:
        return self.name

    # Implements Sortable

    def __lt__(self, other):
        return self.name < other.name
