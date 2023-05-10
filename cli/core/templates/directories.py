# cli:core:templates
from .protocols import DirectoryGenerator, FileGenerator
from cli.core.filesystem import File, Directory


class Generator(DirectoryGenerator, FileGenerator):
    def generate_directory(self, directory: Directory) -> bool:
        for child in directory.children:
            print(child)

        for f in directory.files:
            print(f)

    def generate_file(self, file: File) -> bool:
        print(file.name)
        print(file.content)
