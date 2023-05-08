# cli:core:filesystem
from rich.tree import Tree
from .files import File


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
