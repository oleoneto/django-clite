# cli:core:filesystem
from pathlib import Path
from .filesystem import FileSystem


class File:
    def __init__(self, name: str, template: str, content="", context=dict):
        self.context = context
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
    def content(self) -> str:
        return self._content

    def path(self, parent: str = None) -> str:
        value = self.name if parent is None else f"{parent}/{self.name}"
        return value

    def create(self, parent: str = None):
        # TODO: Perform item creation
        FileSystem().create(self.path(parent), is_dir=False)
        # Path(self.path(parent)).touch(exist_ok=True)

    def __str__(self) -> str:
        return self.name

    # Implements Sortable

    def __lt__(self, other):
        return self.name < other.name
