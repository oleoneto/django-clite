from rich.tree import Tree
from cli.handlers.filesystem.file_handler import FileHandler


class Directory(FileHandler):
    def __init__(self, name, children=[], files=[], templates_scope=None, dry=False, force=False, verbose=False, debug=False):
        super(Directory, self).__init__(dry, force, verbose, debug)

        self.name = name
        self.children = children
        self.files = files
        self.templates_scope = templates_scope

    def __str__(self):
        return f"{self.name}, children: {len(self.children)} files: {len(self.files)}"

    def traverse(self, **kwargs):
        tree = Tree(self.name)

        if kwargs.get('show_files', None):
            for file in self.files:
                tree.add(file.filename)

        for child in self.children:
            child_tree = child.traverse(**kwargs)
            tree.add(child_tree)

        return tree

    def create(self, template_handler, **kwargs):
        return self.create_folder(self, template_handler, **kwargs)
