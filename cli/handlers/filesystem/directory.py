import os
from rich.tree import Tree
from cli.handlers.filesystem.file_handler import FileHandler
from cli.handlers.filesystem.template_handler import TemplateHandler
from cli.handlers.filesystem.template import Template


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

    def add_children(self, children, **kwargs):
        for child in children:
            if not type(child) == type(self):
                child = Directory(name=child)

            self.children.append(child)

    def create(self, template_handler, **kwargs):
        return self.create_folder(self, template_handler, **kwargs)

    @classmethod
    def ensure_directory(cls, container, **kwargs):
        folder = Directory(container, files=[Template('__init__.py', '# import package modules here', raw=True)])

        if container not in os.listdir():
            folder.create(template_handler=TemplateHandler(), **kwargs)
        else:
            if '__init__.py' not in os.listdir(container):
                if kwargs.get('no_append', False):
                    return

                os.chdir(container)

                folder.create_file(filename='__init__.py', content='# import package modules here', **kwargs)

                os.chdir('..')
