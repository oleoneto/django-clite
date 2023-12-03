# cli:core:filesystem
from typing import Self
from pathlib import Path
from rich.tree import Tree
from rich.text import Text
from .files import File
from .protocols import FileProtocol
from .filesystem import FileSystem


class Directory:
    def __init__(self, name: str, children: [FileProtocol] = None):
        self.name = name
        self._children = []

        if children is not None:
            self.add_children(children)

    def add_children(self, dirs: list[FileProtocol]):
        dirs = dirs if dirs is not None else []
        [self._children.append(f) for f in dirs if type(f) in [Directory, File]]

    @property
    def dirs(self) -> list[Self]:
        return [f for f in self._children if type(f) is Directory]

    @property
    def files(self) -> list[File]:
        return [f for f in self._children if type(f) is File]

    def print(self, **kwargs):
        """
        A printable representation of the directory structure and its content.
        """
        from rich import print as r

        r(self.tree(**kwargs))

    def tree(self, **kwargs):
        name = Path(self.name)
        tree = Tree(name.__str__())

        for child in sorted(self.dirs):
            child_tree = child.tree(**kwargs)
            if child_tree is None:
                continue
            tree.add(child_tree)

        if kwargs.get("hide_files", False):
            return tree

        for file in sorted(self.files):
            filepath = file.name
            filename = Text(filepath.__str__())
            filename.stylize(f"link file://{filepath}")
            tree.add(filename)

        return tree

    def path(self, parent: str = None) -> str:
        value = self.name if parent is None else f"{parent}/{self.name}"
        return value

    def create(self, parent=None):
        # Create top-level directory
        path = self.path(parent=parent)

        # TODO: Perform item creation
        FileSystem().create(path, is_dir=True)

        # Recursively create children items
        for child in self._children:
            child.create(parent=path)

    def __str__(self) -> str:
        return self.name

    # Implements Sortable

    def __lt__(self, other):
        return self.name < other.name
